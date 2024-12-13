import uuid

from unigate.models.base import GroupBase
from unigate.schemas.student import StudentReadWithoutGroups
from pydantic import BaseModel

class GroupRead(GroupBase):
    id: uuid.UUID


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
