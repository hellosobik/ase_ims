from flask import *
import sqlite3
import string 
import random 
import smtplib
# from flask_sqlalchemy import SQLAlchemy
import datetime
import json
import os

os.environ["FLASK_DEBUG"] = "1"
os.environ["FLASK_APP"] = "app"

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ase.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

# db = SQLAlchemy(app)
# app.secret_key = "abc" 

def db_connection():
    conn=None
    try:
        conn = sqlite3.connect("ase.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn
# class create_stock(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     item_names = db.Column(db.String(200), nullable = False)
#     item_qtys = db.Column(db.String(200), nullable = False)
#     time = db.Column(db.String(200), nullable = False)


# class read_stock(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     item_names = db.Column(db.String(200), nullable = False)
#     item_qtys = db.Column(db.String(200), nullable = False)
#     time = db.Column(db.String(200), nullable = False)


# class update_stock(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     item_names = db.Column(db.String(200), nullable = False)
#     item_qtys = db.Column(db.String(200), nullable = False)
#     time = db.Column(db.String(200), nullable = False)



# class each_day_history(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     item_names = db.Column(db.String(200), nullable = False)
#     item_qtys = db.Column(db.String(200), nullable = False)
#     time = db.Column(db.String(200), nullable = False)

# class amartya_sold(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     item_names = db.Column(db.String(200), nullable = False)
#     item_qtys = db.Column(db.String(200), nullable = False)
#     time = db.Column(db.String(200), nullable = False)

# class sobik_sold(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     item_names = db.Column(db.String(200), nullable = False)
#     item_qtys = db.Column(db.String(200), nullable = False)
#     time = db.Column(db.String(200), nullable = False)

# class amartya_consumed(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     item_names = db.Column(db.String(200), nullable = False)
#     item_qtys = db.Column(db.String(200), nullable = False)
#     time = db.Column(db.String(200), nullable = False)

# class sobik_consumed(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     item_names = db.Column(db.String(200), nullable = False)
#     item_qtys = db.Column(db.String(200), nullable = False)
#     time = db.Column(db.String(200), nullable = False)

# class items_lost(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     item_names = db.Column(db.String(200), nullable = False)
#     item_qtys = db.Column(db.String(200), nullable = False)
#     time = db.Column(db.String(200), nullable = False)

#{'item_name_0': 'bournvita', 'item_quantity_0': '20', 'item_name_1': 'oreo', 'item_quantity_1': '30', 'item_name_2': 'bourbon', 'item_quantity_2': '50', 'item_name_3': 'namkeen', 'item_quantity_3': '60'}

@app.route('/', methods=["POST", "GET"])
def index():
    conn=db_connection()
    cursor = conn.cursor()
    wel_mes="welcome to amartya shoubhik enterprise"
    if request.method == 'POST':
        cursor = conn.execute("")
        result = dict(request.form)
        lst_item_name=[]
        lst_item_quantity=[]
        for i in range(0, int(len(result)/2)):
            lst_item_name.append(result["item_name_"+str(i)])
        for i in range(0, int(len(result)/2)):
            lst_item_quantity.append(result["item_quantity_"+str(i)])
        print(lst_item_name)
        print(lst_item_quantity)
        sqlite_query = """INSERT INTO create_stock
                          (item_names, item_qtys, time) 
                          VALUES (?, ?, ?);"""
        data_tuple=(str(lst_item_name), str(lst_item_quantity), str(datetime.datetime.now()))
        cursor = conn.execute(sqlite_query, data_tuple)
        conn.commit()
        # new_stock = create_stock(item_names="str(lst_item_name)", item_qtys=str(lst_item_quantity), time=str(datetime.datetime.now()))
        # db.session.add(new_stock)
        # db.session.commit()
        print("commit successfull")
        # Send result data to result_data HTML file
        return render_template("index.html", result=result)
    return render_template("index.html", result={"welcome to":"ASE"})

@app.route('/create_stock', methods=["POST", "GET"])
def create_stock():

    return render_template("create_stock.html")