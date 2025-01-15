import datetime
import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship  # type: ignore

from unigate.models.base import DBUnigateBase, GroupBase, UUIDBase
from unigate.models.block import Block
from unigate.models.join import Join
from unigate.models.super_student import SuperStudent

if TYPE_CHECKING:
    from unigate.models.request import Request
    from unigate.models.student import Student


class Group(DBUnigateBase, UUIDBase, GroupBase, table=True):
    __tablename__ = "groups"  # type: ignore

    creator_id: uuid.UUID = Field(
        foreign_key="students.id", nullable=False, ondelete="CASCADE"
    )

    creator: "Student" = Relationship(back_populates="created_groups")

    students: list["Student"] = Relationship(back_populates="groups", link_model=Join)
    super_students: list["Student"] = Relationship(
        back_populates="super_groups", link_model=SuperStudent
    )
    requests: list["Request"] = Relationship(back_populates="group")
    blocked_students: list["Student"] = Relationship(
        back_populates="blocked_groups", link_model=Block
    )
