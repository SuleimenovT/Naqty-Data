# Zadacha2.1

def avg_check(revenue, orders):
    return round(revenue / orders)


print(avg_check(91650, 8))


# Zadacha3.1

def total_with_vat(amount):
    return round(amount + (amount * 0.12))


print(total_with_vat(5650))


# Zadacha4.1

def share(part, total=40):
    return round(part/total * 100, 1)


print(share(8))


# Zadacha5.1

def avg_check(revenue, orders):
    return round(revenue / orders)


def city_report(city, revenue, orders):
    check = avg_check(revenue, orders)
    return f'{city}: {orders} заказов,средний чек {check} tenge'


print(city_report('Shymkent', 11100, 5))

# Zadacha6.1

cities = [
    {'city': 'Astana', 'orders': 9, 'revenue': 48240},
    {'city': 'Алматы',  'orders': 10, 'revenue': 104290},
    {'city': 'Шымкент', 'orders': 5,  'revenue': 11100},
]


def avg_check(revenue, orders):
    return revenue / orders


for ci in cities:
    if avg_check(ci['revenue'], ci['orders']) > 5000:
        print(ci['city'])

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ДОМАШНЕЕ ЗАДАНИЕ
# HW1


def revenue_per_day(revenue, days):
    return round(revenue / days)


print(revenue_per_day(305620, 90))

# HW2


def discount(price, percent=10):
    new_price = price - price * percent / 100
    return round(new_price)


print(discount(2490))
print(discount(2490, 25))

# HW3


def segment(price):
    if price > 3000:
        return 'Premium'
    elif price > 1000:
        return 'Sredniiy'
    else:
        return 'Econome'


print(segment(4500))
print(segment(2490))
print(segment(690))

# HW4

numbers = [4500, 1250, 390]


def segment(numbers):
    if numba > 3000:
        return 'Premium'
    elif numba > 1000:
        return 'Sredniiy'
    else:
        return 'Econome'


for numba in numbers:
    print(numba, segment(numba))

# HW5


def avg_check(revenue, orders):
    return round(revenue / orders)


def city_report(city, revenue, orders):
    check = avg_check(revenue, orders)
    share = orders / 40 * 100
    return f'{city}: {orders} заказов, средний чек {check} tenge, доля {share} %'


print(city_report('Karaganda', 91650, 8))
