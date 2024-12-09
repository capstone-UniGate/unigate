import uuid

from sqlmodel import SQLModel


# Response model for the Student model
class StudentResponse(SQLModel):
    id: uuid.UUID
    name: str
    surname: str


# Response model for the Request model
class RequestResponse(SQLModel):
    id: uuid.UUID
    status: str
    student_id: uuid.UUID
    group_id: uuid.UUID
    student: StudentResponse | None
