# FlyRank Task API

A simple CRUD API built with Python and FastAPI for the FlyRank Internship Backend Track Week 2 Assignment A1.

## Features

- Get all tasks
- Get a single task
- Create a task
- Update a task
- Delete a task
- Input validation
- 404 handling for unknown tasks
- Swagger UI documentation
- In-memory data storage

## Technologies

- Python
- FastAPI
- Uvicorn
- Pydantic

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/FaizanAli615?tab=repositories
cd flyrank-task-api

## Stage 4 — SQLite Verification

I verified that changes made directly in DB Browser for SQLite are immediately visible through the FastAPI API without restarting the server.

Example SQL query:

```sql
SELECT * FROM tasks WHERE done = 1;