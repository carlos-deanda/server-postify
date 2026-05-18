from datetime import datetime
from typing import TYPE_CHECKING, List
import uuid

from pydantic import Field
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from app.schemas.like import LikeRead
    from app.schemas.comment import CommentRead
    

class PostCreate(SQLModel):
    description: str
    user_id: uuid.UUID


class PostRead(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    created_at: datetime
    like_count: int = 0
    comments_count: int = 0


class PostReadDetails(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    created_at: datetime
    likes: List['LikeRead'] = Field(default_factory=list)
    comments: List['CommentRead'] = Field(default_factory=list)


from app.schemas.like import LikeRead
from app.schemas.comment import CommentRead

PostReadDetails.model_rebuild()

    
