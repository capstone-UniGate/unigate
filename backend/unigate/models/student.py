import uuid
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel  # type: ignore

if TYPE_CHECKING:
    from .request import Request


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

    # Reverse relationship to Request
    requests: list["Request"] = Relationship(back_populates="student")
