import datetime
import uuid

from pydantic import EmailStr
from sqlalchemy.orm import registry
from sqlmodel import Column, Enum, Field, SQLModel  # type: ignore

from unigate.enums import GroupType


class DBAuthBase(SQLModel, registry=registry()):
    pass


class DBUnigateBase(SQLModel, registry=registry()):
    pass


class UUIDBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class UserBase(SQLModel):
    number: int = Field(unique=True, index=True, nullable=False, ge=0, le=9999999)
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    name: str = Field(nullable=False)
    surname: str = Field(nullable=True)


class AuthUserBase(UserBase):
    hashed_password: str = Field(nullable=False, index=True)


class GroupBase(SQLModel):
    name: str
    description: str | None = None
    category: str | None = None
    type: GroupType = Field(sa_column=Column(Enum(GroupType, name="group_type")))
    course_name: str
    exam_date: datetime.date | None = None


class RequestBase(SQLModel):
    student_id: uuid.UUID = Field(foreign_key="students.id", ondelete="CASCADE")
    group_id: uuid.UUID = Field(foreign_key="groups.id", ondelete="CASCADE")


class CourseBase(SQLModel):
    name: str = Field(nullable=False, unique=True, index=True)


class ExamBase(SQLModel):
    course_id: uuid.UUID = Field(foreign_key="courses.id", ondelete="CASCADE")
    date: datetime.date
