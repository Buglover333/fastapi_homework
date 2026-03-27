# api/routers/taskmanager.py
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List
from schemas.task import Task

task_router = APIRouter()
tasks = []
counter = 0

def get_tasks_list():
    return tasks

test_tasks = ["Купить продукты", "Сделать ДЗ", "Позвонить маме"]
for text in test_tasks:
    counter += 1
    tasks.append(Task(task_id=counter, task_text=text))

@task_router.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@task_router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((t for t in tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail={"error": {"code": "TaskNotFound", "message": "Task not found"}})
    return task

@task_router.post("/tasks", response_model=Task, status_code=201)
def create_task(task_text: str, task_deadline: datetime = None):
    global counter
    counter += 1
    task = Task(task_id=counter, task_text=task_text, task_deadline=task_deadline)
    tasks.append(task)
    return task

@task_router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_text: str = None, task_deadline: datetime = None):
    task = next((t for t in tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail={"error": {"code": "TaskNotFound", "message": "Task not found"}})
    
    if task_text:
        task.task_text = task_text
    if task_deadline:
        task.task_deadline = task_deadline
    
    return task

@task_router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    global tasks
    task = next((t for t in tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail={"error": {"code": "TaskNotFound", "message": "Task not found"}})
    
    tasks = [t for t in tasks if t.task_id != task_id]
    return None

@task_router.get("/")
def root():
    return {"message": "Task API", "endpoints": "/tasks"}