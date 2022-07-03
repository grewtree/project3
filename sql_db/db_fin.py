import psycopg2

conn = psycopg2.connect(
    host = "arjuna.db.elephantsql.com",
    database = "xwhpjlgi",
    user = "xwhpjlgi",
    password = "dKa8FEUHU27RzxJDPelBs4xFKFRY0uF5" 
)

cur = conn.cursor()

## kospi DB 구축

cur.execute("DROP TABLE IF EXISTS kospi;")
cur.execute("""CREATE TABLE kospi(
            year int,
            month int,
            kospi float
            );
""")

import pandas as pd

df_kospi = pd.read_csv('./data/kospi_p3.csv', encoding='utf-8')

for i in list(range(0, len(df_kospi))) : 
    cur.execute("""INSERT INTO kospi ( year, month, kospi)
                VALUES (%s,%s,%s)""", list(df_kospi.iloc[i]))


## rate(원달러 환율) DB 구축

cur.execute("DROP TABLE IF EXISTS rate;")
cur.execute("""CREATE TABLE rate(
            year int,
            month int,
            rate float
            );
""")

df_rate = pd.read_csv('./data/rate_p3.csv', encoding='utf-8')

for i in list(range(0, len(df_rate))) : 
    cur.execute("""INSERT INTO rate ( year, month, rate)
                VALUES (%s,%s,%s)""", list(df_rate.iloc[i]))

## 금리 DB 구축

cur.execute("DROP TABLE IF EXISTS interest;")
cur.execute("""CREATE TABLE interest(
            year int,
            month int,
            interest float
            );
""")

df_interest = pd.read_csv('./data/interest_p3.csv', encoding='utf-8')
df_interest = df_interest.ffill() #결측치 앞선 값으로 채우기

for i in list(range(0, len(df_interest))) : 
    cur.execute("""INSERT INTO interest ( year, month, interest)
                VALUES (%s,%s,%s)""", list(df_interest.iloc[i]))


## 국제 유가(두바이유) DB 구축

cur.execute("DROP TABLE IF EXISTS oilprice;")
cur.execute("""CREATE TABLE oilprice(
            year int,
            month int,
            oilprice float
            );
""")

df_oil = pd.read_csv('./data/oil_p3.csv', encoding='utf-8')

for i in list(range(0, len(df_oil))) : 
    cur.execute("""INSERT INTO oilprice ( oilprice, year, month )
                VALUES (%s,%s,%s)""", list(df_oil.iloc[i]))

## 소비자물가지수 DB 구축

cur.execute("DROP TABLE IF EXISTS consumerprice;")
cur.execute("""CREATE TABLE consumerprice(
            year int,
            month int,
            consumerprice float
            );
""")

df_consume = pd.read_csv('./data/consumerprice_p3.csv', encoding='utf-8')

df_consume['시점'] = df_consume['시점'].astype(str)

df_consume['year'] = None
df_consume['month'] = None

i= 0 
while i < len(df_consume):
    df_consume['year'].iloc[i] = df_consume['시점'].iloc[i].split("-")[0]
    df_consume['month'].iloc[i] = df_consume['시점'].iloc[i].split("-")[1]
    i += 1
    
df_consume = df_consume.drop('시점', axis = 1)

for i in list(range(0, len(df_consume))) : 
    cur.execute("""INSERT INTO consumerprice ( consumerprice, year, month )
                VALUES (%s,%s,%s)""", list(df_consume.iloc[i]))


## 생산자물가지수 DB 구축

cur.execute("DROP TABLE IF EXISTS productprice;")
cur.execute("""CREATE TABLE productprice(
            year int,
            month int,
            productprice float
            );
""")

df_product = pd.read_csv('./data/productprice_p3.csv', encoding='utf-8')

df_product['시점'] = df_product['시점'].astype(str)

df_product['year'] = None
df_product['month'] = None

i= 0 
while i < len(df_product):
    df_product['year'].iloc[i] = df_product['시점'].iloc[i].split("-")[0]
    df_product['month'].iloc[i] = df_product['시점'].iloc[i].split("-")[1]
    i += 1
    
df_product = df_product.drop('시점', axis = 1)

for i in list(range(0, len(df_product))) : 
    cur.execute("""INSERT INTO productprice ( productprice, year, month )
                VALUES (%s,%s,%s)""", list(df_product.iloc[i]))

conn.commit()



