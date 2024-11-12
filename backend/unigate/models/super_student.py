import uuid

from sqlmodel import Field, SQLModel  # type: ignore


class SuperStudent(SQLModel, table=True):
    __tablename__ = "super_students"  # type: ignore

    student_id: uuid.UUID = Field(
        foreign_key="students.id", primary_key=True, ondelete="CASCADE"
    )
    group_id: uuid.UUID = Field(
        foreign_key="groups.id", primary_key=True, ondelete="CASCADE"
    )
