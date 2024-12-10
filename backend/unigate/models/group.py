import enum
import uuid
from typing import TYPE_CHECKING

from sqlmodel import Column, Enum, Field, Relationship, SQLModel  # type: ignore

from unigate.models.base import DBUnigateBase, UUIDBase
from unigate.models.join import Join

if TYPE_CHECKING:
    from unigate.models.student import Student


class GroupType(str, enum.Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"


class GroupBase(SQLModel):
    name: str
    description: str | None = None
    category: str | None = None
    type: GroupType = Field(sa_column=Column(Enum(GroupType, name="group_type")))

class GroupTest(SQLModel):
    name: str


class Group(DBUnigateBase, UUIDBase, GroupBase, table=True):
    __tablename__ = "groups"  # type: ignore

    creator_id: uuid.UUID = Field(
        foreign_key="students.id", nullable=False, ondelete="CASCADE"
    )
    creator: "Student" = Relationship(back_populates="groups")

    students: list["Student"] = Relationship(back_populates="groups", link_model=Join)
