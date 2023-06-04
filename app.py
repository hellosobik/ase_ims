from flask import *
import sqlite3
import string 
import random 
import smtplib
import datetime
import json
import os
import crud

os.environ["FLASK_DEBUG"] = "1"
os.environ["FLASK_APP"] = "app"

app = Flask(__name__)

def db_connection():
    conn=None
    try:
        conn = sqlite3.connect("ase.sqlite", check_same_thread=False)
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/', methods=["POST", "GET"])
def index():
    conn=db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':

        result = list(dict(request.form).items())
        investment=result[-2:]
        items=result[0:len(result)-2]
        lst_item_name=[]
        lst_item_quantity=[]
        for i in range(0, len(items)):
            if i%2==0:
                lst_item_name.append(items[i][1])
            else:
                lst_item_quantity.append(items[i][1])
        sqlite_query_1=crud.current_stock(str(datetime.datetime.now()).split()[0])
        print(sqlite_query_1)
        sqlite_query_2=crud.sql_query_list["read_current_stock"]
        sqlite_query_3=crud.sql_query_list["insert_new_stock"]
        if "UPDATE" not in sqlite_query_1:

        
        # for i in range(0, int(len(items)/2)):
        #     lst_item_quantity.append(items["item_quantity_"+str(i)])
        # sqlite_query = """INSERT INTO create_stock
        #                   (item_names, item_qtys, time) 
        #                   VALUES (?, ?, ?);"""
            data_tuple=(str(lst_item_name), str(lst_item_quantity), str(datetime.datetime.now()))
            cursor = conn.execute(sqlite_query_1, data_tuple)
        else:
            data=cursor.execute("""
                SELECT * FROM current_stock
                WHERE time Like '{date}%';
                """).fetchall()
            for i in lst_item_name:
                if i in data[0][0][1]:
                    ind_db=data[0][0][1].index("i")
                    ind_in=lst_item_name.index("i")
                    data_ind_db=int(data[0][0][2][ind_db])
                    data_ind_db+=int(lst_item_quantity[ind_in])
                    data[0][0][2][ind_db]=str(data_ind_db)
                else:
                    ind_in=lst_item_name.index("i")
                    data[0][0][1].append(i)
                    data[0][0][2].append(lst_item_quantity[ind_in])
            item_names=data[0][0][1]
            item_qtys=data[0][0][2]
            time=datetime.datetime.now()
            # data_tuple=(str(lst_item_name), str(lst_item_quantity), str(datetime.datetime.now()))
            cursor = conn.execute(sqlite_query_1)
        
        data_tuple=(str(lst_item_name), str(lst_item_quantity), str(investment), str(datetime.datetime.now()))
        cursor = conn.execute(sqlite_query_3, data_tuple)
        data = conn.execute(sqlite_query_2).fetchall()

        conn.commit()
        # return render_template("index.html", result=result)
        # return render_template("index.html", items=(lst_item_name, lst_item_quantity), investment=investment)
        return render_template("index.html", items=data, investment=investment)

    else:
        return render_template("index.html", items="No Items", investment="No investment")

@app.route('/create_stock', methods=["POST", "GET"])
def create_stock():

    return render_template("create_stock.html")