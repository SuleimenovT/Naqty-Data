import pandas as pd

# 2.1

df = pd.read_csv('dala_orders.csv')
# print(df.head())
# print(df.tail(3))

# 3.1

# print(df[['order_id', 'product', 'qty']].head())

# 4.1
# df['amount_vat'] = (df['qty'] * df['price'] * 1.12).round(0)
# print(df['amount_vat'].sum())

# 5.1

# astana = df[df['city'] == 'Астана']
# print(len(astana))
# print((astana['price'] * astana['qty']).sum())

# 5.2
# dairy = df[(df['category'] == 'Молочные продукты') & (df['price'] > 1000)]
# print(len(dairy))

# 6.1
# low3 = df.sort_values('amount').head(3)
# print(low3[['order_id', 'product', 'amount']])

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ДОМАШНЕЕ ЗАДАНИЕ
# HW1

print(len(df[df['qty'] >= 5]))

# HW2

meat = df[df["category"] == "Мясо"]

print(len(meat))
print((meat["price"] * meat["qty"]).sum())

# HW3

feb = df[df["date"].str.startswith("2026-02")]

print((feb["price"] * feb["qty"]).sum())

# HW4

top1 = df.sort_values('amount', ascending=False).head(1)
top1[['order_id', 'city', 'product', 'amount']]


# HW5

def get_size(amount):
    if amount > 10000:
        return 'крупный'
    else:
        return 'обычный'


df['size'] = df['amount'].apply(get_size)

print((df['size'] == 'крупный').sum())
