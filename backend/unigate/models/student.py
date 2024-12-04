import uuid
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel  # type: ignore


class GroupType(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


# TODO: to use as a better way to handle roles
class UserRole(str, Enum):
    STUDENT = "student"
    SUPERST = "superstudent"
    TEACHER = "teacher"


class Student(SQLModel, table=True):
    __tablename__ = "students"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    number: int = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    surname: str = Field(default=None, max_length=255)
