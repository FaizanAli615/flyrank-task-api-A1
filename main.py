from typing import Optional

from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel, Field
import sqlite3

app=FastAPI()
DATABASE='tasks.db'



def get_db():
    connection=sqlite3.connect(DATABASE)
    connection.row_factory=sqlite3.Row
    return connection

def init_db():
    connection=get_db()
    connection.execute(''' Create table if not exists tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,done INTEGER NOT NULL DEFAULT 0) ''')


def seed_tasks():
    connection=get_db()

    count=connection.execute('select count(*) from tasks').fetchone()[0]
    if count==0:
        connection.executemany('''Insert into tasks(title,done) VALUES(?,?)''',[
                ("Learn FastAPI", 0),
                ("Build CRUD API", 0),
                ("Test API with Swagger", 1),
            ] )

        connection.commit()
    connection.close()

init_db()
seed_tasks()

@app.get('/')
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get('/health')
async def health():
    return {'status': 'OK'}

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Test API with Swagger",
        "done": True
    }
]

@app.get("/tasks")
def get_tasks():
    connection = get_db()

    rows = connection.execute(
        "SELECT id, title, done FROM tasks ORDER BY id"
    ).fetchall()

    connection.close()

    tasks = [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]

    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    connection = get_db()

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }



class TaskCreate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        description="The title of the task"
    )


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    if task_data.title is None:
        raise HTTPException(
            status_code=400,
            detail="Task title is required"
        )

    title = task_data.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    connection = get_db()

    cursor = connection.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, 0)
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "id": task_id,
        "title": title,
        "done": False
    }

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        description="New task title"
    )
    done: Optional[bool] = Field(
        default=None,
        description="Whether the task is completed"
    )


@app.put("/tasks/{id}")
def update_task(id: int, task_data: TaskUpdate):
    if task_data.title is None and task_data.done is None:
        raise HTTPException(
            status_code=400,
            detail="Request body must contain title or done"
        )

    connection = get_db()

    existing_task = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    if existing_task is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    title = existing_task["title"]
    done = existing_task["done"]

    if task_data.title is not None:
        title = task_data.title.strip()

        if not title:
            connection.close()

            raise HTTPException(
                status_code=400,
                detail="Task title cannot be empty"
            )

    if task_data.done is not None:
        done = int(task_data.done)

    connection.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (title, done, id)
    )

    connection.commit()
    connection.close()

    return {
        "id": id,
        "title": title,
        "done": bool(done)
    }

@app.delete(f"/tasks/{id}", status_code=204)
def delete_task(id: int):
    connection = get_db()

    existing_task = connection.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    if existing_task is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return