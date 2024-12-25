from typing import TYPE_CHECKING

from sqlmodel import Relationship  # type: ignore

from unigate.models.base import CourseBase, DBAuthBase, UUIDBase
from unigate.models.teach import Teach

if TYPE_CHECKING:
    from unigate.models.auth import AuthUser
    from unigate.models.exam import Exam


class Course(DBAuthBase, UUIDBase, CourseBase, table=True):
    __tablename__ = "courses"  # type: ignore

    professors: list["AuthUser"] = Relationship(
        back_populates="courses", link_model=Teach
    )
    exams: list["Exam"] = Relationship(back_populates="course")
