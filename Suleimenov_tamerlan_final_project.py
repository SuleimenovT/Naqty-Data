#Final Project Suleimenov Tamerlan 

#4.1 Постановка задачи

#Данные: результаты Олимпийских игр 1896-2016 (Kaggle), около 270 000 записей об участниках.

#Главный вопрос: как менялся состав участников и кто лидирует по медалям?

#Вопросы для анализа:
#1. Как менялась доля женщин среди участников по годам?
#2. Какие страны выиграли больше всего медалей?
#3. Есть ли связь между ростом и весом спортсменов?



#4.2 Extract: загрузка данных

import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#4.2.1 Импорт и загрузка

raw = pd.read_csv("athlete_events.csv")
countries = pd.read_csv("country_definitions.csv")
print("Основная таблица:", raw.shape)
print("Справочник стран:", countries.shape)
print('---------------------------------------------')
#4.2.2 Размер, первые строки и типы

print("Строк:", raw.shape[0], "| Столбцов:", raw.shape[1])
print(raw.head())
raw.info()
print('---------------------------------------------')


#4.2.3 Пропуски в штуках и процентах

missing = raw.isna().sum()
print(pd.DataFrame({"пропусков, шт": missing,"пропусков, %": (missing / len(raw) * 100).round(1)}))
print('---------------------------------------------')

#4.2.4 Дубликаты

n_dup = raw.duplicated().sum()
print("Полных дубликатов:", n_dup, f"({n_dup / len(raw) * 100:.2f}% строк)")
print('---------------------------------------------')

#4.2.5 Проверка ключа для merge (бонус +3)

print("Нет в справочнике:", sorted(set(raw["NOC"]) - set(countries["NOC"])))
print(countries.isna().sum())
print(countries[countries["region"].isna()])
print('---------------------------------------------')

#4.3 Transform: очистка и преобразование

#4.3.1 Копия

df = raw.copy()
rows_before, cols_before = df.shape


#4.3.2 Дубликаты, Удаляем, потому что это одна запись, загруженная дважды

df = df.drop_duplicates()
print("Удалено:", rows_before - len(df), "| Осталось:", len(df))
print('---------------------------------------------')

#4.3.3 Текст. Убираем пробелы по краям и двойные: для pandas "Ivan Petrov" и "Ivan Petrov" — разные значения.

text_cols = df.select_dtypes(include=["object", "string"]).columns
for col in text_cols:
    df[col] = df[col].str.strip().str.replace(r"\s+", " ", regex=True)
print(df["Sex"].unique(), df["Season"].unique())

print('---------------------------------------------')


#4.3.4 Medal. Пусто значит «медали нет». Удалять нельзя, потеряем 85% строк.

df["Medal"] = df["Medal"].fillna("No medal")
print(df["Medal"].value_counts())
print('---------------------------------------------')

#4.3.5 Выбросы (IQR на NumPy). 
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

#4.3.6 Пропуски.
#Заполняем медианой по группе «вид спорта + пол»: рост и вес зависят от них. 
#Берём медиану, а не среднее, потому что она устойчива к выбросам. Если группа пустая, берём медиану по полу, потом общую.

for col in ["Age", "Height", "Weight"]:
    df[col] = df[col].fillna(df.groupby(["Sport", "Sex"])[col].transform("median"))
    df[col] = df[col].fillna(df.groupby("Sex")[col].transform("median"))
    df[col] = df[col].fillna(df[col].median())
print(df[["Age", "Height", "Weight", "Medal"]].isna().sum())

print('---------------------------------------------')


#4.3.7 Типы.
#Дат в виде строк нет (Year уже целое), поэтому datetime не нужен.

df["Age"] = df["Age"].round().astype("int64")
for col in ["Sex", "Season", "Medal"]:
    df[col] = df[col].astype("category")
print(df.dtypes)
print('---------------------------------------------')

#4.3.8 Новые признаки (нужно минимум 3)

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

#4.3.9 Merge со справочником (бонус +3)

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

#4.3.10 Контроль


assert df.duplicated().sum() == 0
assert df[["Age", "Height", "Weight", "Medal", "region"]].isna().sum().sum() == 0
print("Проверка пройдена:", df.shape)

print('---------------------------------------------')

#4.3.11 Таблица «было / стало»

summary = pd.DataFrame({
    "Показатель": ["Строк", "Столбцов", "Дубликатов", "Пропусков Age", "Пропусков Height", "Пропусков Weight"],
    "Было": [raw.shape[0], raw.shape[1], raw.duplicated().sum(),
             raw["Age"].isna().sum(), raw["Height"].isna().sum(), raw["Weight"].isna().sum()],
    "Стало": [df.shape[0], df.shape[1], df.duplicated().sum(),
              df["Age"].isna().sum(), df["Height"].isna().sum(), df["Weight"].isna().sum()],
})

print(summary.to_string(index=False))


print('---------------------------------------------')



#4.4 Load: сохранить очищенные данные в CSV (обязательно)

df.to_csv("athlete_events_clean.csv", index=False)
print("Сохранено:", df.shape)

print('---------------------------------------------')

#4.4.1 SQLite и SQL-запрос (бонус +3)


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


#4.4.2 Загрузить сохранённый файл обратно и проверить, что число строк и столбцов совпадает

check = pd.read_csv("athlete_events_clean.csv")

print("Было в df:      ", df.shape)
print("Загружено назад:", check.shape)

assert check.shape == df.shape, "размеры не совпали"
print("Размеры совпадают")

print('---------------------------------------------')

#4.5 Исследовательский анализ (EDA)

#4.5.1 Описательная статистика по числовым столбцам: describe() и функции NumPy (mean,median, std, percentile);

pd.set_option("display.width", 200)
print(df[["Age", "Height", "Weight", "BMI"]].describe().round(1))

print('---------------------------------------------')


#4.5.2 Функции NumPy: mean, median, std, percentile

for col in ["Age", "Height", "Weight"]:
    x = df[col].to_numpy()
    print(col,
          "| среднее:", round(np.mean(x), 1),
          "| медиана:", np.median(x),
          "| std:", round(np.std(x), 1),
          "| p25, p75, p95:", np.percentile(x, [25, 75, 95]))
    

print('---------------------------------------------')


#4.5.3 Группировки: value_counts

print(df["Sex"].value_counts())
print("Доля женщин:", round((df["Sex"] == "F").mean() * 100, 1), "%")
print(df["Season"].value_counts())

print('---------------------------------------------')

#4.5.4 Группировки: groupby

# доля женщин по годам
female_share = ((df["Sex"] == "F").groupby(df["Year"]).mean() * 100).round(1)
print(female_share.loc[[1900, 1920, 1960, 2000, 2016]])

# медианные рост и вес по видам спорта
by_sport = df.groupby("Sport")[["Height", "Weight"]].median().sort_values("Height")
print(by_sport.head(3))
print(by_sport.tail(3))

# средний возраст по десятилетиям
print(df.groupby("Decade")["Age"].mean().round(1))


print('---------------------------------------------')


#4.5.5 Группировки: pivot_table

pivot = df.pivot_table(index="Decade", columns="Sex", values="ID", aggfunc="count")
print(pivot.tail(5))


print('---------------------------------------------')

#4.5.6 Связь двух числовых признаков: np.corrcoef

r = np.corrcoef(df["Height"], df["Weight"])[0, 1]
print("Корреляция роста и веса:", round(r, 3))


# Проверка: влияет ли заполнение пропусков на корреляцию   <-- НОВЫЙ БЛОК
real = raw.drop_duplicates().dropna(subset=["Height", "Weight"])
r_real = np.corrcoef(real["Height"], real["Weight"])[0, 1]
r_filled = np.corrcoef(df["Height"], df["Weight"])[0, 1]

print("Записей с известными ростом и весом:", len(real))
print("Корреляция на реальных значениях:", round(r_real, 3))
print("Корреляция после заполнения:", round(r_filled, 3))

print('---------------------------------------------')

#4.5.7 Не меньше 5 фактов с цифрами для выводов

# медали по странам без повторов в командных видах
medals = df[df["has_medal"] == 1]
unique_medals = medals.drop_duplicates(["Year", "Season", "Sport", "Event", "Medal", "NOC"])
print("Строк с медалью:", len(medals), "| Уникальных медалей:", len(unique_medals))
print(unique_medals.groupby("region").size().sort_values(ascending=False).head(5))

# число участников по годам
print(df.groupby("Year")["ID"].nunique().loc[[1896, 1960, 2016]])


print('---------------------------------------------')



#4.6 Визуализация
#4.6.1 Линейный график

plt.figure(figsize=(9, 4.5))
plt.plot(female_share.index, female_share.values, marker="o", color="#2F6FDE")
plt.title("Доля женщин среди участников Олимпиад выросла с 0% до 45,5%")
plt.xlabel("Год")
plt.ylabel("Доля женщин, %")
plt.grid(alpha=0.3) 
plt.savefig("graph1_female_share.png", dpi=150, bbox_inches="tight")
plt.show()
# Вывод: в 1896 году женщин не было (0%), в 1900 году их доля 1,7%.
# К 1960 году она выросла до 18,7%, к 2000 году до 39,3%, в 2016 году до 45,5%.

print('---------------------------------------------')


#4.6.2 Столбчатая диаграмма (горизонтальная)

top_countries = unique_medals.groupby("region").size().sort_values(ascending=False).head(10)
top_sorted = top_countries.sort_values()

plt.figure(figsize=(9, 5))
plt.barh(top_sorted.index, top_sorted.values, color="#2F6FDE")
plt.title("Топ-10 стран по числу олимпийских медалей: США лидируют")
plt.xlabel("Число медалей (без повторов в командных видах)")
plt.ylabel("Страна")
plt.xlim(left=0)
plt.savefig("graph2_top_countries.png", dpi=150, bbox_inches="tight")
plt.show()
# Вывод: США выиграли 2 823 медали, это 14,9% всех 18 905 медалей. За ними Россия (1 916)
# и Германия (1 766). В Россию входят СССР и Объединённая команда, как записано в справочнике стран.
print('---------------------------------------------')

#4.6.3 Столбчатая диаграмма (вертикальная, не больше 10 столбцов)


age_by_decade = df[df["Decade"] >= 1920].groupby("Decade")["Age"].mean()

plt.figure(figsize=(9, 4.5))
plt.bar(age_by_decade.index.astype(str), age_by_decade.values, color="#2F6FDE")
plt.title("Средний возраст участников снижался с 1940-х до 1980-х, потом снова вырос")
plt.xlabel("Десятилетие")
plt.ylabel("Средний возраст, лет")
plt.xticks(rotation=45)
plt.ylim(bottom=0)
plt.savefig("graph6_age_decade.png", dpi=150, bbox_inches="tight")
plt.show()
# Вывод: с 28,0 года в 1940-х средний возраст снизился до 23,9 в 1980-х, к 2010-м вырос до 26,1.
# Данные 1890-х и 1900-х не показаны: там мало участников.

print('---------------------------------------------')

#4.6.4 Гистограмма

plt.figure(figsize=(8, 4.5))
plt.hist(df["Age"], bins=30, color="#2F6FDE", edgecolor="white")
plt.axvline(df["Age"].median(), color="black", linestyle="--",
            label=f"Медиана: {df['Age'].median():.0f} лет")
plt.title("Большинство участников Олимпиад моложе 30 лет")
plt.xlabel("Возраст, лет")
plt.ylabel("Количество записей")
plt.legend()
plt.savefig("graph4_age_hist.png", dpi=150, bbox_inches="tight")
plt.show()
# Вывод: медианный возраст 25 лет, моложе 30 лет 80,7% записей. Длинный правый «хвост»
# до 97 лет создают соревнования по искусству.


print('---------------------------------------------')


#4.6.5 Диаграмма рассеяния

sample = df.sample(5000, random_state=42)
plt.figure(figsize=(8, 5))
plt.scatter(sample["Height"], sample["Weight"], s=8, alpha=0.3, color="#2F6FDE")
plt.title(f"Чем выше спортсмен, тем он тяжелее: корреляция {r:.2f}")
plt.xlabel("Рост, см")
plt.ylabel("Вес, кг")
plt.savefig("graph3_height_weight.png", dpi=150, bbox_inches="tight")
plt.show()
# Вывод: корреляция роста и веса 0,798, связь сильная положительная. На графике 5 000 случайных
# записей из 269 731, чтобы точки не сливались. Часть значений заполнена медианой, но на реальных
# значениях корреляция почти такая же (0,796).

print('---------------------------------------------')


#4.6.6 Boxplot

top_sports = df["Sport"].value_counts().head(6).index
data = [df.loc[df["Sport"] == s, "Weight"] for s in top_sports]

plt.figure(figsize=(10, 5))
plt.boxplot(data, tick_labels=list(top_sports))
plt.title("Вес спортсменов в 6 самых массовых видах спорта сильно различается")
plt.xlabel("Вид спорта")
plt.ylabel("Вес, кг")
plt.savefig("graph5_weight_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()
# Вывод: медианный вес: гимнастика 62 кг, лёгкая атлетика 70, плавание 72, фехтование 75, стрельба 77.
# Больше всего выбросов вверх в лёгкой атлетике: толкатели ядра, метатели диска и молота.
print('---------------------------------------------')

#4.6.7 Тепловая карта через imshow

top8 = df["Sport"].value_counts().head(8).index
sub = df[df["Sport"].isin(top8) & (df["Decade"] >= 1960)]
heat = ((sub["Sex"] == "F").groupby([sub["Sport"], sub["Decade"]]).mean() * 100).unstack()

plt.figure(figsize=(9, 5))
plt.imshow(heat.values, cmap="Blues", aspect="auto")
plt.colorbar(label="Доля женщин, %")
plt.xticks(range(len(heat.columns)), heat.columns)
plt.yticks(range(len(heat.index)), heat.index)
for i in range(heat.shape[0]):
    for j in range(heat.shape[1]):
        plt.text(j, i, f"{heat.values[i, j]:.0f}", ha="center", va="center", fontsize=8)
plt.title("Доля женщин растёт во всех массовых видах спорта")
plt.xlabel("Десятилетие")
plt.ylabel("Вид спорта")
plt.savefig("graph7_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()
# Вывод: в велоспорте доля женщин выросла с 0% в 1960-х до 39% в 2010-х, в стрельбе с 0% до 40%,
# в фехтовании с 18% до 50%. Меньше всего изменилась гимнастика: с 38% до 45%.
print('---------------------------------------------')


#4.6.8 Круговая диаграмма

age_counts = df["AgeGroup"].value_counts().reindex(["до 20", "20-29", "30-39", "40+"])

plt.figure(figsize=(6, 6))
plt.pie(age_counts.values, labels=age_counts.index, autopct="%1.1f%%", startangle=90)
plt.title("Две трети участников — в возрасте 20–29 лет")
plt.savefig("graph8_pie.png", dpi=150, bbox_inches="tight")
plt.show()
# Вывод: возраст 20–29 лет у 68,7% записей, 30–39 лет у 16,1%, до 20 лет у 12,0%, старше 40 лет у 3,1%.
print('---------------------------------------------')



#4.6.9 Несколько графиков на одной фигуре: plt.subplots

fig, axes = plt.subplots(2, 2, figsize=(10, 7))
for ax, col, label in zip(axes.ravel(),
                          ["Age", "Height", "Weight", "BMI"],
                          ["Возраст, лет", "Рост, см", "Вес, кг", "Индекс массы тела"]):
    ax.hist(df[col], bins=30, color="#2F6FDE", edgecolor="white")
    ax.set_title(label)
    ax.set_xlabel(label)
    ax.set_ylabel("Количество записей")
fig.suptitle("Распределения возраста, роста, веса и BMI участников")
fig.tight_layout()
plt.savefig("graph9_subplots.png", dpi=150, bbox_inches="tight")
plt.show()
# Вывод: средние значения: возраст 25,5 года, рост 175,6 см, вес 71,0 кг, BMI 22,9. У возраста и веса
# длинный правый «хвост», рост распределён почти симметрично.

print('---------------------------------------------')


#4.7 Выводы

#4.7.1 Ответьте на каждый вопрос 

# Ответ на вопросы

#1. Как менялась доля женщин среди участников по годам?
#Доля женщин выросла с нуля почти до половины. На первых Играх 1896 года среди
#176 участников женщин не было (0%). В 1900 году их доля составила 1,7%, в 1920 году
#3,1%. Заметный рост начался после Второй мировой войны: 18,7% в 1960 году,
#39,3% в 2000 году и 45,5% в 2016 году. За всё время женщины составили 27,6%
#записей (74 378 из 269 731): низкая доля в ранние годы снижает общий показатель.

#Рост был неравномерным по видам спорта. В велоспорте доля женщин выросла
#с 0% в 1960-х до 39% в 2010-х, в стрельбе с 0% до 40%, в фехтовании с 18% до 50%.
#Меньше всего изменилась гимнастика: с 38% до 45%.

#2. Какие страны выиграли больше всего медалей?
#Лидер по числу медалей — США: 2823 медали, это 14,9% от всех 18905 медалей.
#На втором месте Россия 1916, на третьем Германия 1766, затем Великобритания
#919 и Франция 879.
#В командных видах спорта медаль записана каждому участнику команды, поэтому по
#строкам получается 39 772 «медали». Настоящих медалей, если убрать повторы по году,
#виду спорта, соревнованию и стране, 18 905. Для сравнения стран использован
#именно второй показатель.
#Лидер менялся по десятилетиям. В 1950–1960-х впереди Россия 183 и 345 медалей,
#в 1970–1980-х Германия 283 и 416, а с 1990-х лидируют США (246 в 1990-х,
#361 в 2000-х и 289 в 2010-х).

#3. Есть ли связь между ростом и весом спортсменов?
#Да, связь сильная и положительная: коэффициент корреляции равен 0,798.
#Чем выше спортсмен, тем он в среднем тяжелее. Это видно и на диаграмме
#рассеяния: точки вытянуты вдоль диагонали.
#Разница между видами спорта большая. Медианный рост и вес у баскетболистов
#193 см и 89 кг, у гимнастов 167 см и 62 кг. Средние значения по всем участникам:
#рост 175,6 см, вес 71,0 кг, индекс массы тела 22,9.



#4.7.2 Написать ограничения данных: за какой период они собраны, чего в них нет


#- Период. Данные охватывают Олимпийские игры с 1896 по 2016 год. Более поздних
#  Игр в них нет, поэтому выводы не описывают современное положение.
#- Пропуски. Рост был пропущен у 22,2% записей, вес у 23,2%, возраст у 3,5%.
#  Я заполнил их медианой по виду спорта и полу. Это оценка, а не измерение.
#  Проверка: на 206 840 записях, где рост и вес известны, корреляция 0,796,
#  а после заполнения 0,798, то есть заполнение почти не повлияло на результат.
#- Страны. В справочнике «Россия» включает СССР и Объединённую команду,
#  «Германия» включает ГДР и ФРГ. Поэтому сравнение стран по десятилетиям
#  нужно воспринимать осторожно.
#- Чего нет в данных. В них нет населения стран, расходов на спорт и числа
#  дисциплин в каждый год. Данные показывают, кто выигрывал, но не объясняют, почему.
#- Выбросы. Возраст до 97 лет относится к соревнованиям по искусству. Я не удалял
#  эти значения, а пометил флагами. Они немного тянут средний возраст вверх.

#4.7.3 Предложить решение или что исследовать дальше

#Доля женщин почти достигла паритета (45,5% в 2016 году), но в части видов спорта
#разрыв остаётся: например, в велоспорте женщины составляют 39%. Практический вывод
#для организаторов и федераций: внимание стоит уделить видам спорта, где доля женщин
#заметно ниже средней.

#Что исследовать дальше:
#1. Добавить данные о числе женских дисциплин в программе каждой Олимпиады, чтобы
#   понять, растёт ли доля женщин из-за новых дисциплин или из-за большего числа
#   участниц в старых.
#2. Сравнить число медалей с населением и расходами стран на спорт, чтобы оценить
#   эффективность, а не только абсолютный результат.
#3. Проверить связь роста и веса отдельно по видам спорта, чтобы отделить влияние
#   вида спорта от общей закономерности.