from sqlmodel import SQLModel
from typing import List, Optional
import uuid

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
    student: Optional[StudentResponse]

