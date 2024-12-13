import uuid

from sqlmodel import Field, SQLModel  # type: ignore


class Blocked(SQLModel, table=True):
    __tablename__ = "blocks"  # type: ignore

    student_id: uuid.UUID = Field(
        foreign_key="students.id", primary_key=True, ondelete="CASCADE"
    )
    group_id: uuid.UUID = Field(
        foreign_key="groups.id", primary_key=True, ondelete="CASCADE"
    )
