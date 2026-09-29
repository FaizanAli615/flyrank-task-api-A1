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

    if tasks:
        next_id = max(task["id"] for task in tasks) + 1
    else:
        next_id = 1

    new_task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


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
    # Find the task
    task = None

    for existing_task in tasks:
        if existing_task["id"] == id:
            task = existing_task
            break

    # Task not found
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    # At least one field must be provided
    if task_data.title is None and task_data.done is None:
        raise HTTPException(
            status_code=400,
            detail="Request body must contain title or done"
        )

    # Update title if provided
    if task_data.title is not None:
        title = task_data.title.strip()

        if not title:
            raise HTTPException(
                status_code=400,
                detail="Task title cannot be empty"
            )

        task["title"] = title

    # Update done if provided
    if task_data.done is not None:
        task["done"] = task_data.done

    return task

@app.delete("/tasks/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )