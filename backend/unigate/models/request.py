import enum
import uuid

from sqlmodel import Column, Enum, Field, SQLModel  # type: ignore


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
