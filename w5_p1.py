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