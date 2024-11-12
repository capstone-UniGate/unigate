import enum
import uuid

from sqlmodel import Column, Enum, Field, SQLModel  # type: ignore


class GroupType(str, enum.Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"


class Group(SQLModel, table=True):
    __tablename__ = "groups"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None)
    category: str | None = Field(default=None, max_length=255)
    type: GroupType = Field(sa_column=Column(Enum(GroupType, name="group_type")))

    creator_id: uuid.UUID = Field(
        foreign_key="students.id", nullable=False, ondelete="CASCADE"
    )
