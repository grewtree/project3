import psycopg2

conn = psycopg2.connect(
    host = "arjuna.db.elephantsql.com",
    database = "xwhpjlgi",
    user = "xwhpjlgi",
    password = "dKa8FEUHU27RzxJDPelBs4xFKFRY0uF5" 
)

cur = conn.cursor()

## 지역별 월별 실업자 수 DB 구축

cur.execute("DROP TABLE IF EXISTS unemployment;")
cur.execute("""CREATE TABLE unemployment(
            loc VARCHAR(32),
            year int,
            month int,
            unemployment int
            );
""")

## DB에 넣을 수 있도록 데이터 전처리

import pandas as pd
import mod1

df_unemployment = pd.read_csv('./data/unemployment_p3.csv', encoding='utf-8')

ls = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시','울산광역시', '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도','제주도']

## 빈 데이터프레임 만든 뒤 for문 돌리면서 아래로 concat

df = pd.DataFrame({"unemployment":[], "year":[],"month":[], "loc":[]})


for i in ls :  
    name = i
    df1 = mod1.pre(df_unemployment, name)
    df = pd.concat([df, df1], axis= 0)

df.reset_index(drop = True, inplace=True)

# print(df.loc[1])
# breakpoint()

# 데이터테이블(unemployment)에 값 넣기

for j in list(range(0, len(df))) : 
    cur.execute("""INSERT INTO unemployment ( unemployment, year, month, loc)
                VALUES (%s,%s,%s,%s)""", list(df.loc[j]))

conn.commit()

