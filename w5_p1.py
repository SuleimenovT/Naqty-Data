import numpy as np

#2.1
prices = np.array([590,1390,290,4800,990])

print(prices.shape)
print(prices.dtype)

print('--------------------------------------')
#3.1

import numpy as np
import pandas as pd

df = pd.read_csv('dala_orders.csv')
df['amounts'] = df['price'] * df['qty']

amounts = df['amounts'].to_numpy()
print(amounts[10:15])

print('--------------------------------------')
#4.1

discounted = amounts * 0.9
print(discounted.sum())

print('--------------------------------------')
#4.2

print(np.round(amounts[:5] * 1.12))

print('--------------------------------------')

#5.1
revenue = np.array([
    [28000, 60290, 16000],   # Алматы
    [15000, 33240,     0],   # Астана
    [ 3500,  7600,     0],   # Шымкент
    [27000, 59910,  4740],   # Караганда
    [18250, 32090,     0],   # Актобе
])
print(revenue[:,2])

print('--------------------------------------')

#5.2

print(np.round(revenue[:,1] / revenue[:,0],2))

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ДОМАШНЕЕ ЗАДАНИЕ
# HW1
print('--------------------------------------')

import numpy as np
import pandas as pd

number_orders = np.arange(1,41)
print(number_orders.shape, number_orders[-3:])

# HW2
print('--------------------------------------')


df = pd.read_csv('dala_orders.csv')
prices = df['price'].to_numpy()

print(prices.sum() / prices.size)
# HW3
print('--------------------------------------')

df['amount'] = df['price'] * df['qty']
amounts = df['amount'].to_numpy()


print(np.round(amounts[:4] / 520,2))
# HW4
print('--------------------------------------')

revenue = np.array([
    [28000, 60290, 16000],   # Алматы
    [15000, 33240,     0],   # Астана
    [ 3500,  7600,     0],   # Шымкент
    [27000, 59910,  4740],   # Караганда
    [18250, 32090,     0],   # Актобе
])

print(revenue[3:, :2])


# HW5
print('--------------------------------------')
revenue = np.array([
    [28000, 60290, 16000],   # Алматы
    [15000, 33240,     0],   # Астана
    [ 3500,  7600,     0],   # Шымкент
    [27000, 59910,  4740],   # Караганда
    [18250, 32090,     0],   # Актобе
])

print(revenue[:,0] + revenue[:,1])