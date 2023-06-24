from fastapi import FastAPI

app = FastAPI()

import sqlite3

conn = sqlite3.connect("example.db")
cur = conn.cursor()
cur.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, name TEXT, done BOOLEAN)")
from pydantic import BaseModel

class TaskIn(BaseModel):
    name: str
    done: bool

class TaskOut(BaseModel):
    id: int
    name: str
    done: bool
@app.post("/tasks/", response_model=TaskOut)
async def create_task(task: TaskIn):
    query = "INSERT INTO tasks (name, done) VALUES (?, ?)"
    values = (task.name, task.done)
    cur.execute(query, values)
    task_id = cur.lastrowid
    conn.commit()
    return {**task.dict(), "id": task_id}

@app.get("/tasks/", response_model=list[TaskOut])
async def get_tasks():
    query = "SELECT * FROM tasks"
    cur.execute(query)
    rows = cur.fetchall()
    tasks = [TaskOut(id=row[0], name=row[1], done=row[2]) for row in rows]
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: int):
    query = "SELECT * FROM tasks WHERE id = ?"
    value = (task_id,)
    cur.execute(query, value)
    row = cur.fetchone()
    task = TaskOut(id=row[0], name=row[1], done=row[2])
    return task

@app.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task: TaskIn):
    query = "UPDATE tasks SET name = ?, done = ? WHERE id = ?"
    values = (task.name, task.done, task_id)
    cur.execute(query, values)
    conn.commit()
    return {**task.dict(), "id": task_id}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = "DELETE FROM tasks WHERE id = ?"
    value = (task_id,)
    cur.execute(query, value)
    conn.commit()
    return {"message": f"Task with id {task_id} deleted successfully"}
