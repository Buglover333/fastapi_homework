from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import List
from schemas.task import Task

app = FastAPI()

# типо можно было сделать бд НО Я НЕ БУДУ
tasks = []
counter = 0

test_tasks = ["Купить продукты", "Сделать ДЗ", "Позвонить маме"]
for text in test_tasks:
    counter += 1
    tasks.append(Task(task_id=counter, task_text=text))

# получение задач
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# по АйДи
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((t for t in tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(404, "НЕТУ ТАКОЙ ЗАДАЧИ!!!!!")
    return task

# Новая задача
@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_text: str, task_deadline: datetime = None):
    global counter
    counter += 1
    task = Task(task_id=counter, task_text=task_text, task_deadline=task_deadline)
    tasks.append(task)
    return task

# Обновление задачи
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_text: str = None, task_deadline: datetime = None):
    task = next((t for t in tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(404, "НЕТУ ТАКОЙ ЗАДАЧИ!!!!!")
    
    if task_text:
        task.task_text = task_text
    if task_deadline:
        task.task_deadline = task_deadline
    
    return task

# Удаление задачи
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    global tasks
    task = next((t for t in tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(404, "НЕТУ ТАКОЙ ЗАДАЧИ!!!!!")
    
    tasks = [t for t in tasks if t.task_id != task_id]
    return None


@app.get("/")
def root():
    return {"message": "Task API", "endpoints": "/tasks"}

# типо котики
#  /\___/\
#  \/   \/
#   \~ ~/
#  ==`^ ==
#   /   \        |\___/|
#  /|   |        \/- -\/ ____...,...
#  || - |         \o o/             \
#  ||   |        ==`^ ==   ,        /\
#  ||| ||_            `.  / --- \  / \\____//
# /\||_|//         ;____,'      | /   ` ---
# \_____/                    ;___/