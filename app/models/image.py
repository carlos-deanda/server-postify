
from datetime import datetime
import uuid

from sqlmodel import Field, Relationship, SQLModel 

class Image(SQLModel, table=True):
    __tablename__ = 'images'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str
    post_id: uuid.UUID = Field(foreign_key="posts.id")

    post: "Post" = Relationship(back_populates="images")
