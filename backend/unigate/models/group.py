import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship  # type: ignore

from unigate.models.base import DBUnigateBase, GroupBase, UUIDBase
from unigate.models.join import Join

if TYPE_CHECKING:
    from unigate.models.student import Student
    from unigate.models.join import Join


class Group(DBUnigateBase, UUIDBase, GroupBase, table=True):
    __tablename__ = "groups"  # type: ignore

    creator_id: uuid.UUID = Field(
        foreign_key="students.id", nullable=False, ondelete="CASCADE"
    )
    creator: "Student" = Relationship(back_populates="created_groups")

    students: list["Student"] = Relationship(back_populates="groups", link_model=Join)
