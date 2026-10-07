# zadacha2.1
def spread(amounts):
    return round(max(amounts) - min(amounts))


amounts = [9000, 2490, 2070, 1560, 6400]

print(spread(amounts))

# primer2
orders = [
    {'id': 1,  'city': 'Алматы',    'client': 'Аскар Болатов',   'product': 'Кофе 250 г',
        'category': 'Бакалея',           'qty': 2, 'price': 4500},
    {'id': 2,  'city': 'Астана',    'client': 'Ерлан Сериков',   'product': 'Сыр 300 г',
        'category': 'Молочные продукты', 'qty': 1, 'price': 2490},
    {'id': 3,  'city': 'Алматы',    'client': 'Дана Ахметова',
        'product': 'Молоко 1 л',  'category': 'Молочные продукты', 'qty': 3, 'price': 690},
    {'id': 4,  'city': 'Шымкент',   'client': 'Тимур Оспанов',   'product': 'Багет',
        'category': 'Хлеб',              'qty': 4, 'price': 390},
    {'id': 5,  'city': 'Караганда', 'client': 'Мадина Касымова', 'product': 'Мёд 500 г',
        'category': 'Бакалея',           'qty': 2, 'price': 3200},
    {'id': 6,  'city': 'Астана',    'client': 'Аскар Болатов',
        'product': 'Масло 200 г', 'category': 'Молочные продукты', 'qty': 2, 'price': 1250},
    {'id': 7,  'city': 'Алматы',    'client': 'Ерлан Сериков',   'product': 'Сыр 300 г',
        'category': 'Молочные продукты', 'qty': 2, 'price': 2490},
    {'id': 8,  'city': 'Караганда', 'client': 'Дана Ахметова',   'product': 'Кофе 250 г',
        'category': 'Бакалея',           'qty': 1, 'price': 4500},
    {'id': 9,  'city': 'Шымкент',   'client': 'Тимур Оспанов',
        'product': 'Молоко 1 л',  'category': 'Молочные продукты', 'qty': 2, 'price': 690},
    {'id': 10, 'city': 'Астана',    'client': 'Мадина Касымова', 'product': 'Багет',
        'category': 'Хлеб',              'qty': 3, 'price': 390},
]


def line_amount(order):
    return order['qty'] * order['price']


def revenue(orders):
    total = 0
    for o in orders:
        total = total + line_amount(o)
    return total


print(line_amount(orders[0]))   # один заказ
print(revenue(orders))

# zadacha3.1


def count_items(orders):
    return sum(order['qty'] for order in orders)


print(count_items(orders))


# Zadacha 4.1

def filter_by(orders, key, value):
    return [order for order in orders if order[key] == value]


print(len(filter_by(orders, 'category', 'Молочные продукты')))


# zadacha 5.1

def revenue_by(orders, key):
    result = {}
    for order in orders:
        group = order[key]
        result[group] = result.get(group, 0) + order['qty'] * order['price']
    return result


print(revenue_by(orders, 'category'))

# primer 5

# city_report(orders, city)
# ├── filter_by()   → заказы города
# ├── revenue()     → выручка
# ├── len()         → число заказов
# └── avg_check()   → средний чек


def avg_check(revenue, orders):
    return round(revenue / orders)


def line_amount(order):
    return order['qty'] * order['price']


def revenue(orders):
    total = 0
    for o in orders:
        total = total + line_amount(o)
    return total


def filter_by(orders, key, value):
    result = []
    for o in orders:
        if o[key] == value:
            result.append(o)
    return result


def revenue_by(orders, key):
    result = {}
    for o in orders:
        k = o[key]
        result[k] = result.get(k, 0) + line_amount(o)
    return result


def city_report(orders, city):
    city_orders = filter_by(orders, 'city', city)
    rev = revenue(city_orders)
    n = len(city_orders)
    check = avg_check(rev, n)
    return f'{city}: {n} заказа, выручка {rev} ₸, средний чек {check} ₸'


print(city_report(orders, 'Алматы'))

# zadacha 6.1


def avg_check(revenue, orders):
    return round(revenue / orders)


def line_amount(order):
    return order['qty'] * order['price']


def revenue(orders):
    total = 0
    for o in orders:
        total = total + line_amount(o)
    return total


def filter_by(orders, key, value):
    result = []
    for o in orders:
        if o[key] == value:
            result.append(o)
    return result


def revenue_by(orders, key):
    result = {}
    for o in orders:
        k = o[key]
        result[k] = result.get(k, 0) + line_amount(o)
    return result


def city_report(orders, city):
    city_orders = filter_by(orders, 'city', city)
    rev = revenue(city_orders)
    n = len(city_orders)
    check = avg_check(rev, n)
    return f'{city}: {n} заказа, выручка {rev} ₸, средний чек {check} ₸'


print(city_report(orders, 'Караганда'))


# Zadacha 7.1

def line_amount(order):
    return order['qty'] * order['price']


def revenue_by(orders, key):
    result = {}
    for o in orders:
        k = o[key]
        result[k] = result.get(k, 0) + line_amount(o)
    return result


by_client = revenue_by(orders, 'client')
top = max(by_client, key=by_client.get)
print(top, by_client[top])

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ДОМАШНЕЕ ЗАДАНИЕ
# HW1


def avg_price(orders):
    return round(sum(o['price'] for o in orders) / len(orders))


print(avg_price(orders))

# HW2


def big_orders(orders, limit=4000):
    return [o['id'] for o in orders if o['qty'] * o['price'] > limit]


print(big_orders(orders))
print(big_orders(orders, 5000))

# HW3


def count_by(orders, key):
    result = {}
    for o in orders:
        result[o[key]] = result.get(o[key], 0) + 1
    return result


print(count_by(orders, 'city'))

# HW4


def revenue_by(orders, key):
    result = {}
    for o in orders:
        result[o[key]] = result.get(o[key], 0) + o['qty'] * o['price']
    return result


def avg_check(revenue, count):
    return round(revenue / count)


def avg_check_by(orders, key):
    revenue = revenue_by(orders, key)
    counts = count_by(orders, key)
    return {k: avg_check(revenue[k], counts[k]) for k in revenue}


print(avg_check_by(orders, 'city'))

# HW5


def summary(orders):
    by_city = revenue_by(orders, 'city')
    by_category = revenue_by(orders, 'category')
    total = sum(by_city.values())
    count = len(orders)
    best_city = max(by_city, key=by_city.get)
    best_category = max(by_category, key=by_category.get)
    return (f"Заказов: {count}, выручка {total} ₸, "
            f"средний чек {avg_check(total, count)} ₸, "
            f"лучший город {best_city}, лучшая категория {best_category}")


print(summary(orders))
