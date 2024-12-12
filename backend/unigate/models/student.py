from typing import TYPE_CHECKING

from sqlmodel import Relationship  # type: ignore

from unigate.models.base import DBUnigateBase, UserBase, UUIDBase
from unigate.models.join import Join

if TYPE_CHECKING:
    from unigate.models.group import Group


class Student(DBUnigateBase, UUIDBase, UserBase, table=True):
    __tablename__ = "students"  # type: ignore

    created_groups: list["Group"] = Relationship(
        back_populates="creator",  # type: ignore
    )

    groups: list["Group"] = Relationship(
        back_populates="students",  # type: ignore
        link_model=Join,
    )
