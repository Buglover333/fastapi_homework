from fastapi import FastAPI
from .routers.taskmanager import task_router
from .routers.auth import auth_router

app = FastAPI()
app.include_router(task_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Task API", "endpoints": ["/tasks", "/auth/login"]}