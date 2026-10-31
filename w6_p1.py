import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('dala_orders.csv')
df['amount'] = df['price'] * df['qty']
df['month'] = df['date'].str[:7]

MAIN = '#c7de2f'   # основной цвет — один на весь отчёт
MUTED = '#C5CCD6'   # фон: всё, что не главное

print(df.shape, df['amount'].sum())


daily = df.groupby('date')['amount'].sum().cumsum()

plt.figure(figsize=(9, 4))
plt.plot(daily.index, daily.values, color=MAIN, linewidth=2)
plt.title('Выручка сети за квартал: 305 620 ₸')
plt.xlabel('Дата')
plt.ylabel('Выручка нарастающим итогом, ₸')
plt.xticks(daily.index[::6], rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()



#2.1
print('--------------------------------------------')


monthly = df.groupby('month')['amount'].sum()

plt.figure(figsize=(7, 4))
plt.plot(monthly.index, monthly.values, color=MAIN, linewidth=2, marker='o')
plt.title('Пик выручки — февраль; март ещё не закончился')
plt.xlabel('Месяц')
plt.ylabel('Выручка, ₸')
plt.grid(alpha=0.3)
plt.show()


#3.1
print('--------------------------------------------')

vyruska_category = df.groupby('category')['amount'].sum().sort_values()

plt.figure(figsize=(8, 4))
plt.barh(vyruska_category.index, vyruska_category.values, color=MAIN)
plt.title('Мясо и бакалея — 72 % выручки')
plt.xlabel('Выручка, ₸')
plt.tight_layout()
plt.show()



#4.1
print('--------------------------------------------')

plt.figure(figsize=(7, 4))
plt.hist(df['qty'], bins=6, color=MAIN, edgecolor='white')
plt.title('Чаще всего берут 5–6 штук за раз')
plt.xlabel('Количество в заказе, шт.')
plt.ylabel('Число заказов')
plt.show()


#5.1
print('--------------------------------------------')


plt.figure(figsize=(7, 5))
plt.scatter(df['qty'], df['amount'], color=MAIN, s=60, alpha=0.7)
plt.title('Количество само по себе почти не объясняет сумму')
plt.xlabel('Количество, шт.')
plt.ylabel('Сумма заказа, ₸')
plt.grid(alpha=0.3)
plt.show()

print(df[['price', 'qty', 'amount']].corr().round(2))


#6.1
print('--------------------------------------------')


df.groupby('date')['amount'].sum().cumsum().plot(
    figsize=(9, 4), color=MAIN, title='Выручка нарастающим итогом', ylabel='₸', xlabel='')
plt.show()



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ДОМАШНЕЕ ЗАДАНИЕ
# HW1

Lider = df.groupby('city')['order_id'].count().sort_values()

plt.figure(figsize=(8,4))
plt.barh(Lider.index, Lider.values, color=MAIN)
plt.title('Больше всего заказов — в Алматы и Астане')
plt.xlabel('Число заказов')
plt.tight_layout()
plt.show()

# HW2

Lider_average = df.groupby('city')['amount'].mean().sort_values()

plt.figure(figsize=(8, 4))
plt.barh(Lider_average.index, Lider_average.values, color=MAIN)
plt.title(' Высокий средний чек — в Караганде, заказов меньше')
plt.xlabel('Средний чек, ₸')
plt.tight_layout()
plt.show()


# HW3

Almaty_gistogramma = df[df['city'] == 'Алматы']['amount']

plt.figure(figsize=(7, 4))
plt.hist(Almaty_gistogramma, bins=5, color=MAIN, edgecolor='white')
plt.title('В Алматы заказы разные — от 1450 до 27500 тенге')
plt.xlabel('Сумма заказа, тенге')
plt.ylabel('Число заказов')
plt.show()

# HW4

vyruska_category1 = df.groupby('category')['amount'].sum().sort_values()
colors = [MAIN if c == vyruska_category1.idxmax() else MUTED for c in vyruska_category1.index]

plt.figure(figsize=(8, 4))
plt.barh(vyruska_category1.index, vyruska_category1.values, color=colors)
for i, v in enumerate(vyruska_category1.values):
    plt.text(v + 1500, i, f'{v:,}'.replace(',', ' '), va='center')
plt.title('Мясо — категория сети')
plt.xlabel('Выручка, тенге')
plt.xlim(0, 130000)
plt.tight_layout()
plt.show()


# HW5

vuryska_month = df.groupby('month').agg(revenue=('amount', 'sum'), orders=('order_id', 'count'))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
a1.bar(vuryska_month.index, vuryska_month['revenue'], color=MAIN)
a1.set_title('Выручка, ₸')
a2.bar(vuryska_month.index, vuryska_month['orders'], color=MAIN)
a2.set_title('Число заказов')
fig.suptitle('Февраль впереди по обеим метрикам; данные за март неполные')
plt.tight_layout()
plt.show()