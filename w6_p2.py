#1.1


#Какие 3-5 городов дают наибольшую долю выручки за последние 4 квартала?
#Какие категории товаров дают наибольшую долю выручки, и как она менялась от квартала к кварталу (в процентах)?
#В каких сочетаниях «город × категория» выручка растёт быстрее всего за последние 2 квартала? это вопрос?


#2.1


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

MAIN = '#2F6FDE'
MUTED = '#C5CCD6'

raw = pd.read_csv('dala_orders_raw.csv')



raw.info()

print(raw.isna().sum())

print('---------------------------------------------------')
#Primer2

print('Полных дублей:', raw.duplicated().sum())
raw[raw.duplicated(keep=False)][['order_id', 'date', 'city', 'product', 'qty']]

#3.1

print('---------------------------------------------------')

raw = raw.drop_duplicates()
print(len(raw))


#Primer3

print(raw['city'].unique())
print(raw['city'].nunique(), 'вариантов вместо 5')


print('---------------------------------------------------')

#3.2


raw['city'] = raw['city'].str.strip().str.title()

print(raw['city'].unique())
print(raw['city'].nunique())

print('---------------------------------------------------')


#Primer4

print(raw[raw['price'].isna()][['order_id', 'product', 'price', 'qty']])


print('---------------------------------------------------')


#3.3

prices = (raw.groupby('product')['price'].transform('max'))

raw['price'] = raw['price'].fillna(prices)

print(raw['price'].isna().sum())


print('---------------------------------------------------')


#Primer5

print(raw[raw['qty'] <= 0])

print('---------------------------------------------------')

#3.4

raw = raw[raw['qty'] > 0].copy()

raw['amount'] = raw['qty'] * raw['price']
raw['month'] = pd.to_datetime(raw['date']).dt.to_period('M')

print(len(raw))   # ожидается 40

print('---------------------------------------------------')


#Primer6

assert len(raw) == 40, f'Строк {len(raw)}, а должно быть 40'
assert raw['amount'].sum() == 305620, f"Выручка {raw['amount'].sum()}, а должна быть 305 620"
assert raw['city'].nunique() == 5, 'Городов должно быть 5'
assert raw['price'].isna().sum() == 0, 'Остались пропуски в цене'
print('✅ Сверка пройдена: 40 заказов, 305 620 ₸')


print('---------------------------------------------------')

#4.1

def kpi(data):
    return{
        'revenue': int(data['amount'].sum()), 
        'orders': len(data), 
        'avg_check': round(data['amount'].mean()), 
        'median_check': round(data['amount'].median())
    }

print(kpi(raw))

print('---------------------------------------------------')

#4.2

rows = []

for city,data in raw.groupby('city'):
    row = kpi(data)
    row['city'] = city
    rows.append(row)

city_kpi = (
    pd.DataFrame(rows).set_index('city').sort_values('revenue',ascending=False)

)

print(city_kpi)



print('---------------------------------------------------')


#Razbiraem Vmeste

city_revenue = (
    raw.groupby('city')['amount'].sum().sort_values(ascending=False)

)

city_share = (
    city_revenue / raw['amount'].sum() * 100
).round(1)

print(city_revenue)
print(city_share)


print('---------------------------------------------------')


#5.1

