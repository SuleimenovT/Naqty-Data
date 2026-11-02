#Final Project Suleimenov Tamerlan 

#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt

#df = pd.read_csv("athlete_events.csv")
#countries = pd.read_csv("country_definitions.csv")

#print(df.shape, countries.shape)
#df.info()

#miss = df.isna().sum()
#print(pd.DataFrame({"шт": miss, "%": (miss / len(df) * 100).round(1)}))
#print("Полных дубликатов:", df.duplicated().sum())



# ШАГ 1. Вопрос 

#Данные:** результаты Олимпийских игр 1896-2016 (Kaggle), около 270 000 записей об участниках.

#**Главный вопрос:** как менялся состав участников и кто лидирует по медалям?

#**Вопросы для анализа:**
#1. Как менялась доля женщин среди участников по годам?
#2. Какие страны выиграли больше всего медалей?
#3. Есть ли связь между ростом и весом спортсменов?



# ШАГ 2. Extract: загрузка данных

import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#1. Импорт и Загрузка

raw = pd.read_csv("athlete_events.csv")
countries = pd.read_csv("country_definitions.csv")
print("Основная таблица:", raw.shape)
print("Справочник стран:", countries.shape)
print('---------------------------------------------')
#1.1 Размеры,первые строки и типы

print("Строк:", raw.shape[0], "| Столбцов:", raw.shape[1])
raw.head()
raw.info()
print('---------------------------------------------')


#1.3 Пропуски в штуках и процентах

missing = raw.isna().sum()
print(pd.DataFrame({"пропусков, шт": missing,"пропусков, %": (missing / len(raw) * 100).round(1)}))
print('---------------------------------------------')

#1.4 Дубликаты 

n_dup = raw.duplicated().sum()
print("Полных дубликатов:", n_dup, f"({n_dup / len(raw) * 100:.2f}% строк)")
print('---------------------------------------------')

#1.5 Проверка ключа для merge (бонус +3)

print("Нет в справочнике:", sorted(set(raw["NOC"]) - set(countries["NOC"])))
print(countries.isna().sum())
countries[countries["region"].isna()]
print('---------------------------------------------')

# 2. Transform : очистка и преобразавание 

#2.1 Копия 

df = raw.copy()
rows_before, cols_before = df.shape


#2.2 Дубликаты, Удаляем, потому что это одна запись, загруженная дважды

df = df.drop_duplicates()
print("Удалено:", rows_before - len(df), "| Осталось:", len(df))
print('---------------------------------------------')

#2.3 Текст. Убираем пробелы по краям и двойные: для pandas "Ivan Petrov" и "Ivan Petrov" — разные значения.

text_cols = df.select_dtypes(include=["object", "string"]).columns
for col in text_cols:
    df[col] = df[col].str.strip().str.replace(r"\s+", " ", regex=True)
print(df["Sex"].unique(), df["Season"].unique())

print('---------------------------------------------')


#2.4 Medal. Пусто значит «медали нет». Удалять нельзя, потеряем 85% строк.

df["Medal"] = df["Medal"].fillna("No medal")
print(df["Medal"].value_counts())
print('---------------------------------------------')

#2.5 Выбросы (IQR на NumPy). 
#Ищем до заполнения пропусков, чтобы медианы не искажали границы. 
#Выбросы не удаляем, а помечаем: возраст 97 лет относится к соревнованиям по искусству, это не ошибка.


def iqr_bounds(values):
    x = values.dropna().to_numpy()
    q1, q3 = np.percentile(x, [25, 75])
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr

rows = []
for col in ["Age", "Height", "Weight"]:
    low, high = iqr_bounds(df[col])
    is_out = (df[col] < low) | (df[col] > high)
    df[f"{col}_outlier"] = is_out
    rows.append({"столбец": col, "нижняя": low, "верхняя": high,
                 "выбросов, шт": int(is_out.sum()),
                 "мин": df[col].min(), "макс": df[col].max()})

print(pd.DataFrame(rows).set_index("столбец"))
print()
print(df[df["Age"] >= 60]["Sport"].value_counts().head(5))

print('---------------------------------------------')

#2.6 Пропуски. 
#Заполняем медианой по группе «вид спорта + пол»: рост и вес зависят от них. 
#Берём медиану, а не среднее, потому что она устойчива к выбросам. Если группа пустая, берём медиану по полу, потом общую.

for col in ["Age", "Height", "Weight"]:
    df[col] = df[col].fillna(df.groupby(["Sport", "Sex"])[col].transform("median"))
    df[col] = df[col].fillna(df.groupby("Sex")[col].transform("median"))
    df[col] = df[col].fillna(df[col].median())
print(df[["Age", "Height", "Weight", "Medal"]].isna().sum())

print('---------------------------------------------')


#2.7 Типы. 
#Дат в виде строк нет (Year уже целое), поэтому datetime не нужен.

df["Age"] = df["Age"].round().astype("int64")
for col in ["Sex", "Season", "Medal"]:
    df[col] = df[col].astype("category")
print(df.dtypes)
print('---------------------------------------------')

#2.8 Новые признаки (нужно минимум 3)

df["Decade"] = df["Year"] // 10 * 10
df["BMI"] = (df["Weight"] / (df["Height"] / 100) ** 2).round(1)
df["AgeGroup"] = np.select([df["Age"] < 20, df["Age"] < 30, df["Age"] < 40],
                           ["до 20", "20-29", "30-39"], default="40+")
df["has_medal"] = np.where(df["Medal"] != "No medal", 1, 0)
print(df[["Year", "Decade", "BMI", "Age", "AgeGroup", "has_medal"]].head())
print()
print(df["AgeGroup"].value_counts())
print()
print(df.shape)
print('---------------------------------------------')

#2.9 Таблица «было / стало»

summary = pd.DataFrame({
    "Показатель": ["Строк", "Столбцов", "Дубликатов", "Пропусков Age", "Пропусков Height", "Пропусков Weight"],
    "Было": [raw.shape[0], raw.shape[1], raw.duplicated().sum(),
             raw["Age"].isna().sum(), raw["Height"].isna().sum(), raw["Weight"].isna().sum()],
    "Стало": [df.shape[0], df.shape[1], df.duplicated().sum(),
              df["Age"].isna().sum(), df["Height"].isna().sum(), df["Weight"].isna().sum()],
})

print(summary.to_string(index=False))


print('---------------------------------------------')

#2.10 Merge со справочником (бонус +3)

ref = countries.copy()
ref["region"] = ref["region"].fillna(ref["notes"])
ref = pd.concat([ref, pd.DataFrame([{"NOC": "SGP", "region": "Singapore"}])],
                ignore_index=True)

n_before = len(df)
df = df.merge(ref[["NOC", "region"]], on="NOC", how="left")
assert len(df) == n_before
print("Пустых region:", df["region"].isna().sum())
print(df.shape)
print('---------------------------------------------')
#2.11 Контроль


assert df.duplicated().sum() == 0
assert df[["Age", "Height", "Weight", "Medal", "region"]].isna().sum().sum() == 0
print("Проверка пройдена:", df.shape)

print('---------------------------------------------')


#3 Load: Сохранить очищенные данные в CSV (обязательно)

df.to_csv("athlete_events_clean.csv", index=False)
print("Сохранено:", df.shape)

print('---------------------------------------------')

#3.1 SQLite и SQL-запрос (бонус +3)


conn = sqlite3.connect("olympics.db")
df.to_sql("athletes", conn, if_exists="replace", index=False)
query = """
SELECT region, SUM(has_medal) AS medals
FROM athletes
GROUP BY region
ORDER BY medals DESC
LIMIT 5
"""
print(pd.read_sql(query, conn))
conn.close()


print('---------------------------------------------')


#3.2 Загрузить сохранённый файл обратно и проверить, что число строк и столбцов совпадает

check = pd.read_csv("athlete_events_clean.csv")

print("Было в df:      ", df.shape)
print("Загружено назад:", check.shape)

assert check.shape == df.shape, "размеры не совпали"
print("Размеры совпадают")

print('---------------------------------------------')

#4 Исследовательский анализ (EDA)

