# 1. Сохрани в переменные город (`Астана`), количество заказов (9) и выручку (48240 ₸). Вывести всё одной строкой.

city = "Astana"
orders_count = 9
revenue = 48240

print(f"{city}: {orders_count} заказов, средний чек {revenue: .0f} tenge")


# 2. Посчитать средний чек по Астане и округлить до целого.

avg_check = revenue / orders_count
print(round(avg_check))


# 3. Всего по сети 40 заказов, из них в Шымкенте 5. Посчитать долю Шымкента в процентах с одним знаком после запятой.


all_orders = 40
Shymkent_orders = 5
share = Shymkent_orders / all_orders * 100
print(round(share, 1))


# 4. Собрать f-строкой фразу вида `Шымкент: 5 заказов, доля 12.5%`.


city = "Шымкент"
print(f"{city}: {Shymkent_orders} заказов, доля {share} % ")


# 5. Проверить `type()` у всех созданных переменных и объяснить в комментарии, почему выручка это `int`, а доля `float`.

print(type(city))
print(type(all_orders))
print(type(share))
