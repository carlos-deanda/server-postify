
from datetime import datetime
import uuid

from sqlmodel import Field, Relationship, SQLModel 

class Comment(SQLModel, table=True):
    __tablename__='comments'


    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    user_id: uuid.UUID = Field(foreign_key="users.id")
    post_id: uuid.UUID = Field(foreign_key="posts.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")