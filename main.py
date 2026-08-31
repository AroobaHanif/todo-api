from fastapi import FastAPI

app = FastAPI(title="Task API", version="1.0")


@app.get("/", tags=["Info"], summary="API info")
def root():
    """Describes this API and lists its endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", tags=["Info"], summary="Health check")
def health():
    """Simple liveness check."""
    return {"status": "ok"}
