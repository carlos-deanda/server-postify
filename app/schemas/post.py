from datetime import datetime
import uuid

from sqlmodel import SQLModel

class PostCreate(SQLModel):
    description: str
    user_id: uuid.UUID


class PostRead(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    created_at: datetime
    