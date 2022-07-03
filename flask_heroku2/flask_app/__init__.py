from flask import Flask, render_template, request
import pickle
import lightgbm as lgb
from category_encoders import OneHotEncoder
import pandas as pd
import numpy as np

# import mlmodel

with open("./flask_app/model.pkl", 'rb') as pk : 
    model = pickle.load(pk)

with open("./flask_app/encoder.pkl", 'rb') as pk : 
    encoder = pickle.load(pk)

# 

import psycopg2


## 머신러닝 함수
def lgbm(ls):
    list = pd.DataFrame([ls], columns =['location', 'month', 'kospi', 'interest', 'rate', 'oilprice','productprice', 'consumerprice'])
    X_test = encoder.transform(list)
    y_pred = model.predict(X_test)
    return y_pred

## 앱

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return render_template("index.html")

@app.route("/res/", methods=['GET'])
def res():
    location = request.args.get("location")
    month = request.args.get("month")
    kospi = request.args.get("kospi")
    interest = request.args.get("interest")
    rate = request.args.get("rate")
    oilprice = request.args.get("oilprice")
    consumer = request.args.get("consumer")
    producer = request.args.get("producer")
    ls = [ str(location), str(month), float(kospi), float(interest), float(rate), float(oilprice), float(producer), float(consumer) ]
    list = []
    for i in ls : 
        list.append(i)
    result = lgbm(list)
    res = (round(result[0],4) * 1000)

    ## 이용데이터 DB에 저장

    conn = psycopg2.connect(
    host = "arjuna.db.elephantsql.com",
    database = "xwhpjlgi",
    user = "xwhpjlgi",
    password = "dKa8FEUHU27RzxJDPelBs4xFKFRY0uF5" )

    ls2 = ls
    ls2.append(res)
    cur = conn.cursor()
    cur.execute("""INSERT INTO result ( location, month, kospi, interest, rate, oilprice, producer, consumer,result )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);""", (ls2))
    conn.commit()

    name = request.args.get("location")
    month= request.args.get("month")
    return render_template("res.html", location=name, month=month, result=res)


if __name__ == "__main__":
    app.run(debug=True)
