import enum
import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel  # type: ignore

if TYPE_CHECKING:
    from .student import Student


class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Request(SQLModel, table=True):
    __tablename__ = "requests"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: RequestStatus = Field(
        sa_column=Column(Enum(RequestStatus, name="request_status"))
    )

    student_id: uuid.UUID = Field(foreign_key="students.id", ondelete="CASCADE")
    group_id: uuid.UUID = Field(foreign_key="groups.id", ondelete="CASCADE")

    # Relationship to Student
    student: Optional["Student"] = Relationship(back_populates="requests")
