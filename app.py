from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import crud
import sqlite3
from databases import Database

database = Database("sqlite:///test.db")

app = FastAPI()

class New_stock_tup(BaseModel):
    item_names_qty: dict
    a_s_invest: str
    time: str

@app.get("/")
def root():
    return "todooo"

@app.post("/new_stock")
async def new_stock(new_stock_tup: New_stock_tup):
    conn=sqlite3.connect("ase.sqlite", check_same_thread=False)
    cursor=conn.cursor()
    item_names_qty=dict(eval(new_stock_tup.item_names_qty))
    a_s_invest=new_stock_tup.a_s_invest
    time=new_stock_tup.time
    crud.push_new_stock(item_names_qty, a_s_invest, time) # type: ignore
    conn.commit()
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