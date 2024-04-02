import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Date, insert
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime
import re

engine = sqlalchemy.create_engine("sqlite:///inventory.db", echo=True)
Base = declarative_base()

class product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)
    


def load_data_to_database(csv):
    df = pd.read_csv(csv)
    df['product_price'] = df["product_price"].apply(lambda x: re.sub(r'[^0-9]','', x))
    df.reset_index(drop=True, inplace=True)
    with engine.connect() as conn:
        df.to_sql("product", conn, if_exists="append", index=False)
        conn.commit()

def view_product():
    print("enter product ID:\n")
    id = int(input())
    with engine.connect() as conn:
        query = conn.execute(text(f"SELECT * FROM product WHERE product_id = {id}"))
        print(*query)

def add_product():
    print("Product name: "); name = input()
    print("Product price: "); price = int(input()) 
    print("Product quantity: "); quantity = int(input()) 
    date = datetime.now().date()

    stmt = insert(product).values(product_name = name, product_price = price, product_quantity = quantity, date_updated = date)
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()
        print("INSERT SUCCESSFUL")


def make_backup():
    with engine.connect() as conn:
        backup_df = pd.read_sql_query("SELECT * FROM product",conn)
        backup_df.to_csv("./backup.csv")

action_list = {"v": view_product,
               "a": add_product,
               "b": make_backup}

def create_menu():
    print("\n---------------------------------------\n")
    print("SELECT ACTION:\n\
          v: View details of a product with ID\n\
          a: Add new product\n\
          b: Make backup")
    
    action = input()
    action_list[action]()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    load_data_to_database("store-inventory\inventory.csv")
    while(True):
        create_menu()
