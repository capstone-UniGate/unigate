import datetime
import uuid

from pydantic import BaseModel

from unigate.models.base import GroupBase
from unigate.schemas.student import StudentReadWithoutGroups


class GroupRead(GroupBase):
    id: uuid.UUID
    date: datetime.date


class GroupReadWithStudents(GroupRead):
    students: list[StudentReadWithoutGroups]
    creator: StudentReadWithoutGroups
    super_students: list[StudentReadWithoutGroups]
    blocked_students: list[StudentReadWithoutGroups]


class GroupReadOnlyStudents(BaseModel):
    students: list[StudentReadWithoutGroups]
    super_students: list[StudentReadWithoutGroups]
    blocked_students: list[StudentReadWithoutGroups]


class GroupCreate(GroupBase):
    pass
