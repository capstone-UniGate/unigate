import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from unigate.models.base import DBAuthBase, ExamBase

if TYPE_CHECKING:
    from unigate.models.course import Course


class Exam(DBAuthBase, ExamBase, SQLModel, table=True):
    __tablename__ = "exams"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    course: "Course" = Relationship(back_populates="exams")
