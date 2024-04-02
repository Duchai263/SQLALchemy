import pandas as pd
import re 

df = pd.read_csv("store-inventory/inventory.csv")
df['product_price'] = df["product_price"].apply(lambda x: re.sub(r'[^0-9]','', x))
# print(df["product_price"])

print(df.keys())
