import pandas as pd
import numpy as np
df = pd.read_csv('dala_orders.csv')
df['amount'] = df['price'] * df['qty']

amounts = df['amount'].to_numpy()     # колонка → массив numpy
prices = df['price'].to_numpy()
qty = df['qty'].to_numpy()

print(type(amounts), amounts.shape)
print(amounts[:10])

#2.1
print('------------------------------------------')


print(qty.mean())
print(prices.max())


#3.1
print('------------------------------------------')
revenue = np.array([
    [28000, 60290, 16000],   # Алматы
    [15000, 33240,     0],   # Астана
    [ 3500,  7600,     0],   # Шымкент
    [27000, 59910,  4740],   # Караганда
    [18250, 32090,     0],   # Актобе
])

print(revenue.mean(axis=1).round(1))

#3.2
print('------------------------------------------')

cities = np.array(['Алматы', 'Астана', 'Шымкент', 'Караганда', 'Актобе'])
totals = revenue.sum(axis=1)
print(cities[np.argmax(totals)])


#4.1 
print('------------------------------------------')


#small = amounts < 1000
#print(small.sum())
#print(amounts[small])


cheap = amounts[amounts < 1000]

print(len(cheap))
print(cheap)


#4.2
print('------------------------------------------')



#a = amounts > amounts.mean()
#print(a.sum())
#print(round(amounts[a].sum() / amounts.sum()* 100,1))
avg = amounts.mean()
big = amounts[amounts > avg]

print(len(big))
print(round(big.sum() / amounts.sum() * 100, 1))

#5.1
print('------------------------------------------')

delivery = np.where(amounts >= 5000, 0, 1500)
print(delivery.sum())


#6.1
print('------------------------------------------')




# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ДОМАШНЕЕ ЗАДАНИЕ
# HW1
print('--------------------------------------')


prices = df['price'].to_numpy()

med = np.median(prices)

print(med)
print((prices > med).sum())

# HW2
print('--------------------------------------')


cities = np.array(['Алматы', 'Астана', 'Шымкент', 'Караганда', 'Актобе'])
months = np.array(['Январь', 'Февраль', 'Март'])

# выручка: 5 городов × 3 месяца
revenue = np.array([
    [28000, 60290, 16000],   # Алматы
    [15000, 33240,     0],   # Астана
    [ 3500,  7600,     0],   # Шымкент
    [27000, 59910,  4740],   # Караганда
    [18250, 32090,     0],   # Актобе
])


total = revenue.sum(axis=0)
idx = np.argmax(total)
print(months[idx])

#HW3
print('--------------------------------------')

total_month = revenue.sum(axis=0)
share = total_month[1] / revenue.sum() * 100

print(round(share,1))


#HW4 
print('--------------------------------------')


qty = df['qty'].to_numpy()
amount = df['amount'].to_numpy()



labels = np.where(qty >= 5, 'опт' , 'розница')

opt_amount = amount[labels == 'опт']

print(len(opt_amount))
print(round(opt_amount.mean()))


#HW5 
print('--------------------------------------')

price = df['price'].to_numpy()
amount = df['amount'].to_numpy()

print(round(amounts[prices >= 2000].mean()))