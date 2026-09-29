from fastapi import FastAPI,HTTPException,status

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