from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Comment(BaseModel):
    comment_id: int
    task_id: int
    text: str
    created_at: datetime = datetime.now()

class CommentCreate(BaseModel):
    text: str