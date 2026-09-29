# Zadacha2

prices = [4500, 3990, 2490, 690, 320]
# print(prices[0], prices[-1], len(prices))

# Zadacha3

prices = [4500, 3990, 2490, 690, 320]
print(prices[:2])

# Zadacha4

print(sum(prices))
print(max(prices))

# Zadacha5

demo = [250, 390, 180]
result = demo.append(320)

print(len(demo))

# Zadacha6

bread = [250, 390, 180]
for breads in bread:
    print(f'Хлеб: {breads} tenge')


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ДОМАШНЕЕ ЗАДАНИЕ
# HW1

numbers = [690, 620, 890, 2490]
print(len(numbers), max(numbers), min(numbers))


# HW2

numbers = [690, 620, 890, 2490]

print(numbers[:2])
print(numbers[-1])

# HW3

numbers1 = [690, 620, 890, 2490]
numbers1.remove(620)
numbers1.append(1250)

print(numbers1)
print(len(numbers1))

# HW4

numbers2 = [690, 620, 890, 2490]
print(round(sum(numbers2) / len(numbers2)))


# HW5

numbers3 = [690, 620, 890, 2490]

for numba in numbers3:
    print(f'Молочное: {numba} тенге')
