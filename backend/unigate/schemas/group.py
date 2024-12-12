import uuid

from unigate.models.group import GroupBase
from typing import TYPE_CHECKING

from unigate.schemas.student import StudentReadWithoutGroups

class GroupRead(GroupBase):
    id: uuid.UUID

class GroupReadWithStudents(GroupRead):
    id: uuid.UUID
    students: list[StudentReadWithoutGroups]
    creator: StudentReadWithoutGroups

class GroupCreate(GroupBase):
    pass
