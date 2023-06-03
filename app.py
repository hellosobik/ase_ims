from flask import *
import sqlite3
import string 
import random 
import smtplib
import datetime
import json
import os

os.environ["FLASK_DEBUG"] = "1"
os.environ["FLASK_APP"] = "app"

app = Flask(__name__)

def db_connection():
    conn=None
    try:
        conn = sqlite3.connect("ase.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/', methods=["POST", "GET"])
def index():
    conn=db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        cursor = conn.execute("")
        result = dict(request.form)
        lst_item_name=[]
        lst_item_quantity=[]
        for i in range(0, int(len(result)/2)):
            lst_item_name.append(result["item_name_"+str(i)])
        for i in range(0, int(len(result)/2)):
            lst_item_quantity.append(result["item_quantity_"+str(i)])
        sqlite_query = """INSERT INTO create_stock
                          (item_names, item_qtys, time) 
                          VALUES (?, ?, ?);"""
        data_tuple=(str(lst_item_name), str(lst_item_quantity), str(datetime.datetime.now()))
        cursor = conn.execute(sqlite_query, data_tuple)
        conn.commit()
        return render_template("index.html", result=result)
    return render_template("index.html", result={"welcome to":"ASE"})

@app.route('/create_stock', methods=["POST", "GET"])
def create_stock():

    return render_template("create_stock.html")