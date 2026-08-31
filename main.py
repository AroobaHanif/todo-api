from fastapi import FastAPI, HTTPException

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish FL-01 assignment", "done": True},
    {"id": 3, "title": "Push code to GitHub", "done": False},
]
next_id = 4


@app.get("/", tags=["Info"], summary="API info")
def root():
    """Describes this API and lists its endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", tags=["Info"], summary="Health check")
def health():
    """Simple liveness check."""
    return {"status": "ok"}


@app.get("/tasks", tags=["Tasks"], summary="List all tasks")
def list_tasks():
    """Returns every task in memory."""
    return tasks


@app.get("/tasks/{task_id}", tags=["Tasks"], summary="Get one task")
def get_task(task_id: int):
    """Returns a single task by id, or 404 if it doesn't exist."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
