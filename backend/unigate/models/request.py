import enum
import uuid
from unigate.models.student import Student

from sqlmodel import Column, Enum, Field, SQLModel ,Relationship # type: ignore


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

    # Relationship to Student (forward reference using a string)
    student: "Student" = Relationship(back_populates="requests")
