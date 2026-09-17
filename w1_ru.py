# 1.1
print("Astana", 2026)

# 1.2
zakaz = 40
vyruska = 305620
supermarket = 5
print(zakaz, vyruska, supermarket)


# 2.1
name = "Shymkent"
zakaz = 5
vuryska = 11100
print(name, zakaz, vuryska)

# 2.2
total = 11100
print(total)

total1 = 12000
print(total1)

# 3.1
city = "Astana"
orders_count = 25
revenue = 100000
print(type(city))
print(type(orders_count))
print(type(revenue))

# 3.2
number = ["12", 12, 12.5, True]
print(type(number))

# 4.1
vyruska = 11100
orders_count = 5
print(vyruska / orders_count)

# 4.2
astana_revenue = 48240
total_revenue = 305620
totals = astana_revenue / total_revenue * 100
print(round(totals, 1))


# 5.1
city = "Shymkent"
a = 5
b = 40
c = a / b * 100
print(f"{city}: {a} заказов, доля {c}%")

# 5.2
orders = 40
money = 305620
print(f"Дала Маркет: {orders} заказов, выручка {money}")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ДОМАШНЕЕ ЗАДАНИЕ - НЕДЕЛЯ 1!!!!!!!!!!!!!!!!!!

# HW1
orders = 10
one_person = 104290
print(one_person / orders)

# HW2
print(8 / 40 * 100)

# HW3

city = "Алматы"
orders = 10
share = 25.0
print(f"{city}: {orders} заказов, доля {share}%")

# HW4

buhanka = 250
bulochka = 180
summa = 3 * buhanka + 2 * bulochka
print(summa)
print(type(summa))

# HW5
vyruska = 305620
order = 40
a = vyruska / order
b = vyruska // order
print(a)
print(b)

# HW6
order = 8
vyruska = 91650
check = vyruska / order
print(round(check))

# HW7
a = 8
b = 40
c = a / b * 100
print(round(c, 1))

# HW8
city = "Алматы"
check_almaty = 10429
srednii_check = 7640
check = check_almaty - srednii_check
print(f"{city} выше среднего на {check}")


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#ПРАКТИКА НА НОУТБУКЕ

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
