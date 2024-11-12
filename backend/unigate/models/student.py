import uuid
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel  # type: ignore


class GroupType(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class Student(SQLModel, table=True):
    __tablename__ = "students"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    number: int = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    surname: str = Field(default=None, max_length=255)
