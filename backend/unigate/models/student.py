from typing import TYPE_CHECKING

from sqlmodel import Relationship  # type: ignore

from unigate.models.base import DBUnigateBase, UserBase
from unigate.models.join import Join

if TYPE_CHECKING:
    from unigate.models.group import Group

# TODO: to use as a better way to handle roles
# class UserRole(str, Enum):
#     STUDENT = "student"
#     SUPERST = "superstudent"
#     TEACHER = "teacher"


class Student(DBUnigateBase, UserBase, table=True):
    __tablename__ = "students"  # type: ignore

    groups: list["Group"] = Relationship(
        back_populates="students",  # type: ignore
        link_model=Join,
    )
