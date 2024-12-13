from typing import TYPE_CHECKING

from sqlmodel import Relationship  # type: ignore

from unigate.models.base import DBUnigateBase, UserBase, UUIDBase
from unigate.models.join import Join
from unigate.models.super_student import SuperStudent

if TYPE_CHECKING:
    from unigate.models.group import Group
    from unigate.models.request import Request


class Student(DBUnigateBase, UUIDBase, UserBase, table=True):
    __tablename__ = "students"  # type: ignore

    created_groups: list["Group"] = Relationship(
        back_populates="creator",  # type: ignore
    )

    groups: list["Group"] = Relationship(
        back_populates="students",  # type: ignore
        link_model=Join,
    )
    super_groups: list["Group"] = Relationship(
        back_populates="super_students", link_model=SuperStudent
    )
    requests: list["Request"] = Relationship(
        back_populates="student",  # type: ignore
    )
