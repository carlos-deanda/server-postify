
from datetime import datetime
import uuid

from sqlmodel import SQLModel

class CommentCreate(SQLModel):
    content: str
    user_id: uuid.UUID
    post_id: uuid.UUID

class CommentRead(SQLModel):
    id: uuid.UUID
    content: str
    user_id: uuid.UUID
    post_id: uuid.UUID
    created_at: datetime


