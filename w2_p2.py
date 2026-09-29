
# Zadacha2.1
product = {
    'name': 'Milk 1litr',
    'category': 'Milk products',
    'price': 690,
}
print(product['price'])


# Zadacha3.1
product = {
    'name': 'Milk 1litr',
    'category': 'Milk products',
    'price': 690,
}
print(product.get('weight', 'нет данных'))

# Zadacha5.1


product = {
    'name': 'Milk 1litr',
    'category': 'Milk products',
    'price': 690,
}

for key, value in product.items():
    print(key, '->', value)

# Zadacha 6.1

price = 390

if price > 1000:
    print('Dorogoi tovar')
else:
    print('Obysnyi tovar')


# Zadacha 7.1

price = 1250

if price > 1000:
    print(price, '→ Премиум')
elif price > 1000:
    print(price, '→ Средний')
else:
    print(price, '→ Эконом')


# Zadacha 8.1

products = [
    {'name': 'Молоко 1 л', 'price': 690},
    {'name': 'Сыр 300 г',  'price': 2490},
    {'name': 'Багет',      'price': 390},
]

print(len(products))             # строк в таблице
print(products[2]['price'])


# Zadacha 9.1

products = [
    {'name': 'Moloko 1l', 'price': 690},
    {'name': 'Syr 300g', 'price': 2490},
    {'name': 'Baget', 'price': 390},
]

for p in products:
    if p['price'] < 1000:
        print(p['name'])


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ДОМАШНЕЕ ЗАДАНИЕ
# HW1

client = {
    'name': 'Askar Bolatov',
    'city': 'Astana',
    'age': '25',
}

print(client['city'])
print(len(client))


# HW2

client = {
    'name': 'Askar Bolatov',
    'city': 'Astana',
    'age': '25',
}
print(client.get('bonus', 'нет'))

# HW3

client1 = {
    'name': 'Askar Bolatov',
    'city': 'Astana',
    'age': '25',
}

client1['bonus'] = True
print(len(client1))

# HW4

age1 = 25

if age1 > 35:
    print('Starshaya gruppa')
elif age1 > 25:
    print('Srednyaa gruppa')
else:
    print('Mladshaya gruppa')


# HW5

name_surname = [
    {'name': 'Erlan', 'surname': 'Serikov', 'age': 30},
    {'name': 'Timur', 'surname': 'Ospanov', 'age': 30},
    {'name': 'Tamerlan', 'surname': 'Suleimenov', 'age': 24},
    {'name': 'Ernar', 'surname': 'Erlanuly', 'age': 22},
]


for person in name_surname:
    if person['age'] == 30:
        print(person['name'], person['surname'])
