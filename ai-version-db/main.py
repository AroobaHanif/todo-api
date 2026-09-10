from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from db import connection, init_db

app = FastAPI(title="Task API")


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.on_event("startup")
def startup():
    init_db()


def to_dict(row):
    return {"id": row[0], "title": row[1], "done": bool(row[2])}


@app.get("/tasks")
def list_tasks():
    rows = connection.execute("SELECT * FROM tasks").fetchall()
    return [to_dict(r) for r in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    row = connection.execute("SELECT * FROM tasks WHERE id = " + str(task_id)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return to_dict(row)


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    cursor = connection.execute("INSERT INTO tasks (title) VALUES (?)", (task.title,))
    connection.commit()
    row = connection.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return to_dict(row)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    title = update.title if update.title is not None else row[1]
    done = int(update.done) if update.done is not None else row[2]
    connection.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, task_id))
    connection.commit()
    updated = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return to_dict(updated)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()
