import datetime
import uuid

from sqlmodel import Field, SQLModel  # type: ignore

from unigate.models.base import DBUnigateBase


class Join(DBUnigateBase, SQLModel, table=True):
    __tablename__ = "joins"  # type: ignore

    date: datetime.date | None = Field(default_factory=datetime.date.today)

    student_id: uuid.UUID = Field(
        foreign_key="students.id", primary_key=True, ondelete="CASCADE"
    )
    group_id: uuid.UUID = Field(
        foreign_key="groups.id", primary_key=True, ondelete="CASCADE"
    )
