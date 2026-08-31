# Task API

A small CRUD API for managing a to-do list, built with FastAPI. Data is stored
in memory only (no database) - it resets when the server restarts.

## Run it

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

The API runs at `http://localhost:8000`. Interactive docs (Swagger UI) are at
`http://localhost:8000/docs`.

## Endpoints

| Method | Path            | Description                     |
|--------|-----------------|----------------------------------|
| GET    | `/`             | API info                        |
| GET    | `/health`       | Health check                    |
| GET    | `/tasks`        | List all tasks                  |
| GET    | `/tasks/{id}`   | Get one task (404 if missing)   |
| POST   | `/tasks`        | Create a task (400 if no title) |
| PUT    | `/tasks/{id}`   | Update a task (404 if missing)  |
| DELETE | `/tasks/{id}`   | Delete a task (404 if missing)  |
| GET    | `/stats`        | Task counts (total/done/open)   |
| POST   | `/reset`        | Reset to the 3 seed tasks       |

## Example request

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
```

```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

![Swagger UI](swagger-screenshot.png)

*(screenshot added after testing the full CRUD cycle via "Try it out")*

## The mortality experiment

Restarting the server resets `tasks` back to the 3 seed tasks - anything
created, updated, or deleted during the previous run is gone. This is because
the list lives only in the process's memory, not on disk. It's the reason
Week 3 introduces a real database.

## AI vs me

*(added after completing the Stage 7 bonus - prompted an AI to build the same
API from a fresh spec, ran it, and compared it against this hand-built
version.)*
