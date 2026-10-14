import pandas as pd


#2.1
df = pd.read_csv('dala_orders.csv')
df['amount'] = df['price'] * df['qty']

print(df.groupby('category')['amount'].sum().sort_values(ascending=False))

#2.2

print(df.groupby('city')['client_id'].nunique().sort_values(ascending=False))


#3.1
df['amount'] = df['price'] * df['qty']
df['month'] = df['date'].str[:7]

month = df.groupby('month').agg(
    revenue = ('amount','sum'),
    orders = ('order_id','count')
)

print(month)

#4.1

print(df.groupby('product')['qty'].sum().nlargest(3))

#5.1

clients = pd.read_csv('dala_clients.csv')
df['amount'] = df['price'] * df['qty']

full = df.merge(clients, on='client_id', how='left')

print(full.groupby('name')['amount'].sum().nlargest(3))
df['month'] = df['date'].str[:7]
#6.1

print(pd.pivot_table(
    df,
    index = 'category',
    columns = 'month',
    values = 'order_id',
    aggfunc= 'count',
    fill_value = 0
))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ДОМАШНЕЕ ЗАДАНИЕ
# HW1

city_max = full.groupby('city')['amount'].max().sort_values(ascending=False)
print(city_max)

# HW2

seg = full.groupby('segment').agg(
    revenue=('amount', 'sum'),
    orders=('order_id', 'count'),
    avg_check=('amount', 'mean')
)
seg['avg_check'] = seg['avg_check'].round()

print(seg.sort_values('avg_check', ascending=False))

# HW3
gen = full.groupby('gender').agg(
    revenue=('amount', 'sum'),
    avg_check=('amount', 'mean')
)
gen['avg_check'] = gen['avg_check'].round()

print(gen)
# HW4


pv = pd.pivot_table(
    full,
    index='segment',
    columns='city',
    values='amount',
    aggfunc='sum',
    fill_value=0
)
print(pv)
print(pv.loc['VIP', 'Караганда'])


# HW5
for city in ['Алматы', 'Караганда']:
    part = full[full['city'] == city]
    print(city)
    print(part.groupby('category')['amount'].sum().nlargest(2))
    print()