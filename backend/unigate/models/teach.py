import uuid

from sqlmodel import Field, SQLModel  # type: ignore

from unigate.models.base import DBAuthBase


class Teach(DBAuthBase, SQLModel, table=True):
    __tablename__ = "teaches"  # type: ignore

    professor_id: uuid.UUID = Field(
        foreign_key="users.id", primary_key=True, ondelete="CASCADE"
    )
    course_id: uuid.UUID = Field(
        foreign_key="courses.id", primary_key=True, ondelete="CASCADE"
    )
