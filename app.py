from flask import *
import sqlite3
import string 
import random 
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

os.environ["FLASK_DEBUG"] = "1"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)
app.secret_key = "abc" 

class create_stock(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item_names = db.Column(db.String(200), nullable = False)
    item_qtys = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String(200), nullable = False)

class read_stock(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item_names = db.Column(db.String(200), nullable = False)
    item_qtys = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String(200), nullable = False)


class update_stock(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item_names = db.Column(db.String(200), nullable = False)
    item_qtys = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String(200), nullable = False)



class each_day_history(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item_names = db.Column(db.String(200), nullable = False)
    item_qtys = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String(200), nullable = False)

class amartya_sold(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item_names = db.Column(db.String(200), nullable = False)
    item_qtys = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String(200), nullable = False)

class sobik_sold(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item_names = db.Column(db.String(200), nullable = False)
    item_qtys = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String(200), nullable = False)

class amartya_consumed(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item_names = db.Column(db.String(200), nullable = False)
    item_qtys = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String(200), nullable = False)

class sobik_consumed(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item_names = db.Column(db.String(200), nullable = False)
    item_qtys = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String(200), nullable = False)

class items_lost(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item_names = db.Column(db.String(200), nullable = False)
    item_qtys = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String(200), nullable = False)

@app.route('/', methods=["POST", "GET"])
def index():
    wel_mes="welcome to amartya shoubhik enterprise"
    if request.method == 'POST':
        result = request.form
        
        # Send result data to result_data HTML file
        return render_template("index.html", result=result)
    return render_template("index.html", result={"welcome to":"ASE"})

@app.route('/create_stock', methods=["POST", "GET"])
def create_stock():
    return render_template("create_stock.html")