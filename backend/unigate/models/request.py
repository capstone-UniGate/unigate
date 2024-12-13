import uuid
from typing import TYPE_CHECKING

from sqlmodel import Column, Enum, Field, Relationship, SQLModel  # type: ignore

from unigate.enums import RequestStatus
from unigate.models.base import DBUnigateBase, RequestBase

if TYPE_CHECKING:
    from unigate.models.group import Group
    from unigate.models.student import Student


class Request(DBUnigateBase, RequestBase, SQLModel, table=True):
    __tablename__ = "requests"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: RequestStatus = Field(
        sa_column=Column(Enum(RequestStatus, name="request_status"))
    )

    group: "Group" = Relationship(back_populates="requests")
    student: "Student" = Relationship(back_populates="requests")
