# FlyRank Task Management API

A RESTful CRUD API built with **Python, FastAPI, and PostgreSQL** for the FlyRank Internship Backend Track — Assignment A3.

The project started as an in-memory CRUD API in A1, moved to SQLite in A2, and is now containerized with PostgreSQL using Docker Compose in A3.

## Features

* Create tasks
* Get all tasks
* Get a task by ID
* Update tasks
* Delete tasks
* Input validation
* Proper HTTP status codes
* 404 handling for unknown tasks
* Parameterized PostgreSQL queries
* Automatic database/table creation
* Automatic seed data on first run
* PostgreSQL persistence
* Dockerized FastAPI application
* Dockerized PostgreSQL database
* Persistent Docker volume
* Swagger/OpenAPI documentation

---

## Technologies

* Python 3.10+
* FastAPI
* Uvicorn
* Pydantic
* PostgreSQL
* Psycopg
* Docker
* Docker Compose

---

## Project Structure

```text
flyrank-task-api-A1/
│
├── main.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .env.example
├── .gitignore
├── README.md
│
└── docs/
    ├── swagger.png
    └── database.png
```

> `.env` is intentionally not included in the repository because it contains environment configuration and is ignored by Git.

---

# Getting Started

## Prerequisites

Make sure you have:

* Docker Desktop installed and running
* Git installed

No local PostgreSQL installation is required to run the application because PostgreSQL runs inside Docker.

---

## Clone the Repository

```bash
git clone https://github.com/FaizanAli615/flyrank-task-api-A1.git
cd flyrank-task-api-A1
```

---

## Environment Configuration

Create a `.env` file in the project root if you want to run the application directly outside Docker.

Example:

```env
DATABASE_URL=postgres://postgres:dev@localhost:5432/tasks
```

An example environment file is also included:

```text
.env.example
```

For Docker Compose, the API container connects to PostgreSQL using the Docker service name:

```text
postgres://postgres:dev@db:5432/tasks
```

The database hostname is `db` because `db` is the PostgreSQL service defined in `compose.yaml`.

---

# Run the Application

The complete application stack can be started with one command:

```bash
docker compose up --build
```

This starts:

* FastAPI API
* PostgreSQL database

The API will be available at:

```text
http://localhost:8000
```

---

# Swagger API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://localhost:8000/docs
```

You can use Swagger's **Try it out** functionality to test all CRUD endpoints.

![Swagger UI](docs/swagger.png)

---

# API Endpoints

| Method | Endpoint      | Description     | Success Status |
| ------ | ------------- | --------------- | -------------: |
| GET    | `/`           | API information |            200 |
| GET    | `/health`     | Health check    |            200 |
| GET    | `/tasks`      | Get all tasks   |            200 |
| GET    | `/tasks/{id}` | Get task by ID  |            200 |
| POST   | `/tasks`      | Create a task   |            201 |
| PUT    | `/tasks/{id}` | Update a task   |            200 |
| DELETE | `/tasks/{id}` | Delete a task   |            204 |

### Error Status Codes

| Status | Meaning              |
| -----: | -------------------- |
|    400 | Invalid request body |
|    404 | Task not found       |

---

# API Examples

## 1. Get API Information

```bash
curl -i http://localhost:8000/
```

Expected response:

```text
HTTP/1.1 200 OK
```

```json
{
  "name": "Task API",
  "version": "1.0",
  "endpoints": [
    "/tasks"
  ]
}
```

---

## 2. Health Check

```bash
curl -i http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## 3. Get All Tasks

```bash
curl -i http://localhost:8000/tasks
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
  },
  {
    "id": 2,
    "title": "Build CRUD API",
    "done": false
  },
  {
    "id": 3,
    "title": "Test API with Swagger",
    "done": true
  }
]
```

---

## 4. Get a Task by ID

```bash
curl -i http://localhost:8000/tasks/1
```

Example response:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "done": false
}
```

If the task does not exist:

```bash
curl -i http://localhost:8000/tasks/999
```

The API returns:

```text
404 Not Found
```

---

## 5. Create a Task

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn PostgreSQL\"}"
```

Expected status:

```text
201 Created
```

Example response:

```json
{
  "id": 4,
  "title": "Learn PostgreSQL",
  "done": false
}
```

New tasks are created with `done: false`.

---

## 6. Update a Task

```bash
curl -i -X PUT http://localhost:8000/tasks/4 \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn PostgreSQL with FastAPI\",\"done\":true}"
```

Expected status:

```text
200 OK
```

Example response:

```json
{
  "id": 4,
  "title": "Learn PostgreSQL with FastAPI",
  "done": true
}
```

---

## 7. Delete a Task

```bash
curl -i -X DELETE http://localhost:8000/tasks/4
```

Expected status:

```text
204 No Content
```

The successful DELETE response has an empty body.

---

# Database

The application uses **PostgreSQL** for persistent storage.

The PostgreSQL database is automatically created through Docker Compose.

Database configuration:

```text
Database: tasks
Username: postgres
Password: dev
Host: db
Port: 5432
```

The `tasks` table is automatically created when the application starts.

The table contains:

| Column  | Type    | Description       |
| ------- | ------- | ----------------- |
| `id`    | SERIAL  | Primary key       |
| `title` | TEXT    | Task title        |
| `done`  | BOOLEAN | Completion status |

---

# Seed Data

When the `tasks` table is empty, the application automatically inserts three initial tasks:

```text
1. Learn FastAPI
2. Build CRUD API
3. Test API with Swagger
```

The seed data is inserted **only when the table is empty**.

Existing tasks are not replaced when the application restarts.

---

# PostgreSQL Persistence

PostgreSQL data is stored using a Docker named volume.

The Compose configuration uses:

```yaml
volumes:
  - taskdata:/var/lib/postgresql/data
```

This means database data survives container restarts.

For example:

```bash
docker compose down
```

Then:

```bash
docker compose up -d
```

Previously created tasks remain available.

![PostgreSQL Database](docs/database.png)

---

# Parameterized SQL

Database queries use PostgreSQL parameterized placeholders such as:

```python
WHERE id = %s
```

and values are supplied separately:

```python
(id,)
```

This avoids directly inserting user-provided values into SQL queries.

---

# Docker Services

The application is composed of two Docker services:

```text
┌──────────────────────────────┐
│       Docker Compose         │
│                              │
│  ┌──────────────┐            │
│  │     API      │            │
│  │   FastAPI    │            │
│  │    :8000     │            │
│  └──────┬───────┘            │
│         │                    │
│         │ db:5432            │
│         ▼                    │
│  ┌──────────────┐            │
│  │  PostgreSQL  │            │
│  │    :5432     │            │
│  └──────┬───────┘            │
│         │                    │
│         ▼                    │
│     taskdata volume          │
│                              │
└──────────────────────────────┘
```

### API Service

The API service builds from the project's `Dockerfile`.

```text
Python + FastAPI + Uvicorn
```

### Database Service

The database service uses the official PostgreSQL Docker image.

```text
PostgreSQL
Database: tasks
```

---

# Useful Docker Commands

### Start the application

```bash
docker compose up --build
```

### Start in detached mode

```bash
docker compose up -d
```

### View running services

```bash
docker compose ps
```

### View API logs

```bash
docker compose logs api
```

### View database logs

```bash
docker compose logs db
```

### Stop the application

```bash
docker compose down
```

### Stop containers and remove the database volume

> Warning: this deletes the PostgreSQL data stored in the Docker volume.

```bash
docker compose down -v
```

---

# Verify PostgreSQL Directly

You can connect to the PostgreSQL container with:

```bash
docker compose exec db psql -U postgres -d tasks
```

Then:

```sql
SELECT * FROM tasks;
```

Exit PostgreSQL with:

```sql
\q
```

---

# Testing

The API was tested using:

* FastAPI Swagger UI
* `curl`
* Docker Compose
* PostgreSQL inside Docker
* Direct PostgreSQL queries

The CRUD flow was verified as:

```text
Create
  ↓
Read
  ↓
Update
  ↓
Read
  ↓
Delete
  ↓
Read / 404
```

The application also was tested for database persistence by stopping and restarting the Docker Compose stack.

---

# Assignment Progression

This project represents the progression of the FlyRank Backend Internship assignments:

### A1 — In-Memory CRUD

The initial version implemented the CRUD API using an in-memory task list.

### A2 — SQLite

The second version replaced in-memory storage with SQLite and added persistent database storage.

### A3 — Docker + PostgreSQL

The current version replaces SQLite with PostgreSQL and runs the complete stack through Docker Compose.

```text
A1
In-Memory
   ↓
A2
SQLite
   ↓
A3
PostgreSQL + Docker Compose
```

---

# Git Commits

The project was developed incrementally through separate stages:

```text
Stage 0: Postgres in Docker + gitignore
Stage 1: connect FastAPI to Postgres
Stage 2: read tasks from Postgres
Stage 3: full CRUD on Postgres
Stage 4: Dockerize API and Postgres
Stage 5: complete documentation and submission
```

---

