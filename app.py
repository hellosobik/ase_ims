from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import crud
import sqlite3
from databases import Database

conn = Database("sqlite:///ase.sqlite")
cursor=conn
app = FastAPI()


#CRUD

import sqlite3
import datetime
conn=sqlite3.connect("ase.sqlite", check_same_thread=False)
from pprint import pprint
cursor=conn.cursor()

conn = Database("sqlite:///ase.sqlite")
cursor=conn

"""
functions to perform
create and update operations
"""

def get_current_stock(time):
    date=str(time).split()[0]

    data=cursor.fetch_all("""
    SELECT * FROM current_stock
    WHERE time Like '{}%';
    """.format(date))
    data=data
    # print(data)
    return data

def add_sub(task, item_names_qty, time):
    item_names_qty=dict(eval(item_names_qty))
    if len(cursor.fetch_all("SELECT * FROM current_stock"))==0: # type: ignore
        item_names_qty_past=dict()
        item_names_qty_past=item_names_qty
        # print(item_names_qty_past)
        # print("current stock is 0")
        return str(item_names_qty_past)
    elif len(get_current_stock(time))==0 and task=="sub": # type: ignore
        item_names_qty_past=dict(eval(cursor.fetch_all("SELECT * FROM current_stock")[-1][-2])) # type: ignore
        for i in item_names_qty.keys():
            if i in item_names_qty_past:
                item_names_qty_past[i]-=item_names_qty[i]
            # item_names_qty_past.update(item_names_qty)
            # print(item_names_qty_past)
        return str(item_names_qty_past)
    elif len(get_current_stock(time))==0 and task=="add": # type: ignore
        item_names_qty_past=dict(eval(cursor.fetch_all("SELECT * FROM current_stock")[-1][-2])) # type: ignore
        for i in item_names_qty.keys():
            if i in item_names_qty_past:
                item_names_qty_past[i]+=item_names_qty[i]
            else:
                item_names_qty_past[i]=item_names_qty[i]
            # item_names_qty_past.update(item_names_qty)
            # print(item_names_qty_past)
        return str(item_names_qty_past)
    else:
        # print("current stock is not 0")
        item_names_qty_past=dict(eval(get_current_stock(time)[0][1])) # type: ignore
        if task=="add":
            for i in item_names_qty.keys():
                if i in item_names_qty_past:
                    item_names_qty_past[i]+=item_names_qty[i]
                else:
                    item_names_qty_past[i]=item_names_qty[i]
            # item_names_qty_past.update(item_names_qty)
            # print(item_names_qty_past)
            return str(item_names_qty_past)
        elif task =="sub":
            for i in item_names_qty_past.keys():
                if i in item_names_qty:
                    item_names_qty_past[i]-=item_names_qty[i]
            # item_names_qty_past.update(item_names_qty)
            # print(item_names_qty_past)
            return str(item_names_qty_past)

        

async def update_current_stock(item_names_qty, time):
    
    data = get_current_stock(time)
    date=str(time).split()[0]

    if len(data)>0: # type: ignore
        await cursor.execute("""
        UPDATE current_stock SET
        item_names_qty = ?,
        time = ?
        WHERE time Like ?
        """, (item_names_qty, time, date+'%')) # type: ignore

        return "success in updation"
    else:
        await cursor.execute("""
        INSERT INTO current_stock 
        (item_names_qty, time)
        VALUES (?,?);
        """, (item_names_qty, time)) # type: ignore

        return "success in insertion"
    
async def push_new_stock(item_names_qty, a_s_invest, time):
    
    await cursor.execute("""
    INSERT INTO new_stock 
    (item_names_qty, a_s_invest, time)
    VALUES (?,?,?);
    """, (item_names_qty, a_s_invest, time)) # type: ignore

    item_names_qty=add_sub(task="add", item_names_qty=item_names_qty, time=time)

    await update_current_stock(item_names_qty, time)

    return "new stock push to inventory"

async def record_change_in_stock(item_names_qty, person_updated, event, time):
    await cursor.execute("""
    INSERT INTO change_in_stock 
    (item_names_qty, person_updated, event, time)
    VALUES (?,?,?,?);
    """, (item_names_qty, person_updated, event, time)) # type: ignore
    item_names_qty=add_sub(task="sub", item_names_qty=item_names_qty, time=time)
    await update_current_stock(item_names_qty, time)
    return "change in stock recorded"

async def delete_table_data():
    await cursor.execute("DELETE FROM change_in_stock")
    await cursor.execute("DELETE FROM current_stock")
    await cursor.execute("DELETE FROM new_stock")
    return("tables erased")

"""
functions to perform read opeations
"""
async def read_past_tranctions(num):
    no_of_rows=int(cursor.fetch_one("SELECT COUNT(*) FROM change_in_stock")[0]) # type: ignore
    num1=no_of_rows/10
    start_id=(num*10)+ 1
    if num == num1:
        end_id=no_of_rows 
    else:
        end_id=(num+1)*10
    results=cursor.fetch_all("""SELECT * FROM 
    change_in_stock WHERE sno 
    BETWEEN ? AND ?""", 
    (start_id, end_id))[::-1] # type: ignore
    return results

async def current_day_sale(time, person, qty):
    date=str(time).split()[0]
    today=cursor.fetch_all("""SELECT * FROM current_sale
    WHERE time LIKE '{}%';
    """.format(date))

    users=cursor.fetch_all("""SELECT DISTINCT person_updated
     FROM change_in_stock WHERE
       time LIKE '{}%'""".format(date))

    users_lst=list()
    for i in users: # type: ignore
        pprint(i)
        users_lst.append(i[0])

    if len(today)==0: # type: ignore
        await cursor.execute("""INSERT INTO current_sale
        (item_person_qty, time) VALUES (?,?) WHERE
        time LIKE ?;""", (date)) # type: ignore
    

    
    return users_lst
    

item_names_qty=str({"gooday":1, "parle":3, "bourbon":4, "namkeen":6, "cake":8})

# time=str(datetime.datetime.now())
# a_s_invest=10000
# time='2023-06-31 20:38:49.970614'
# person_updated="amartya"
# event="sold"

def task():

    # msg=update_current_stock(item_names_qty=item_names_qty, time=time)
    # print(msg)

    # msg=push_new_stock(item_names_qty=item_names_qty, time=time, a_s_invest=a_s_invest)
    # print(msg)

    # msg=record_change_in_stock(item_names_qty=item_names_qty, person_updated=person_updated, event=event, time=time)
    # print(msg)

    # print("")
    current_stock_table=cursor.fetch_all("SELECT * FROM current_stock")
    new_stock_table=cursor.fetch_all("SELECT * FROM new_stock")
    change_in_stock_table=cursor.fetch_all("SELECT * FROM change_in_stock")
    pprint("current_stock_table")
    pprint(current_stock_table)
    pprint("new_stock_table")
    pprint(new_stock_table)
    pprint("change_in_stock_table")
    pprint(change_in_stock_table)

    # print(dict(eval(get_current_stock(time)[0][1])))

# delete_table_data()
# task()
# pprint(read_past_tranctions(num=1))
# pprint(cursor.execute("SELECT * FROM current_stock").fetchall())
# item_names_qty_past=cursor.execute("SELECT * FROM current_stock").fetchall()[-1][-2]
# print(item_names_qty_past)

# for i in range(0,5):
#     task()

# pprint(current_day_sale(time=time))

# conn.commit()
# conn.close()






class New_stock_tup(BaseModel):
    item_names_qty: dict
    a_s_invest: str
    time: str

@app.get("/")
def root():
    return "todooo"

@app.post("/new_stock")
async def new_stock(new_stock_tup: New_stock_tup):
    await cursor.connect()
    item_names_qty=str(new_stock_tup.item_names_qty)
    a_s_invest=new_stock_tup.a_s_invest
    time=new_stock_tup.time
    crud.push_new_stock(item_names_qty, a_s_invest, time) # type: ignore
    return "success"

@app.get("/todo/{id}")
def read_todo(id: int):
    return "read todo item with id {id}"

@app.put("/todo/{id}")
def update_todo(id: int):
    return "update todo item with id {id}"

@app.delete("/todo/{id}")
def delete_todo(id: int):
    return "delete todo item with id {id}"

@app.get("/todo")
def read_todo_list():
    return "read todo list"