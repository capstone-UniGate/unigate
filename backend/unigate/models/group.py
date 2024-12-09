import enum
import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from unigate.models.base import UUIDBase
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
    type: GroupType
    creator_id: uuid.UUID


class GroupTest(SQLModel):
    name: str


class Group(UUIDBase, GroupBase, table=True):
    __tablename__ = "groups"  # type: ignore

    creator_id: uuid.UUID = Field(
        foreign_key="students.id", nullable=False, ondelete="CASCADE"
    )
    creator: "Student" = Relationship(back_populates="groups")

    students: list["Student"] = Relationship(back_populates="groups", link_model=Join)
