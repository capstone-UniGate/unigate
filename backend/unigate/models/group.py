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
    members_count: int = Field(default=0)

    creator_id: uuid.UUID = Field(
        foreign_key="students.id", nullable=False, ondelete="CASCADE"
    )

    @property
    def is_super_student(self) -> bool:
        # TODO: It should be dynamic after login implementation
        return False

    @property
    def is_member_of(self) -> bool:
        # TODO: It should be dynamic after login implementation
        return False
