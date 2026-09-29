from typing import Optional

from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel, Field

app=FastAPI()

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
    return tasks

@app.get('/tasks/{id}')
async def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    else:
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

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
