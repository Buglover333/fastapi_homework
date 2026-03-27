# api/routers/comments.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.comment import Comment, CommentCreate
from api.routers.taskmanager import get_tasks_list

comment_router = APIRouter()
comments = []
comment_counter = 0

def get_comments_list():
    return comments

@comment_router.post("/v1/tasks/{task_id}/comments", response_model=Comment, status_code=201)
def create_comment(task_id: int, comment_data: CommentCreate, tasks: list = Depends(get_tasks_list)):
    task = next((t for t in tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail={"error": {"code": "TaskNotFound", "message": "Task not found"}})
    
    global comment_counter
    comment_counter += 1
    comment = Comment(
        comment_id=comment_counter,
        task_id=task_id,
        text=comment_data.text
    )
    comments.append(comment)
    return comment

@comment_router.get("/v1/tasks/{task_id}/comments", response_model=List[Comment])
def get_comments(task_id: int, tasks: list = Depends(get_tasks_list)):
    task = next((t for t in tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail={"error": {"code": "TaskNotFound", "message": "Task not found"}})
    
    task_comments = [c for c in comments if c.task_id == task_id]
    return task_comments