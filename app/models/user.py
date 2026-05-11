
from datetime import datetime 
import uuid

from sqlmodel import Field, SQLModel
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"



    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    name: str
    lastname: str
    email: str = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)