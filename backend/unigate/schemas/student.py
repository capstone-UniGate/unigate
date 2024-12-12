from unigate.models.base import UserBase
import uuid
from typing import TYPE_CHECKING

from unigate.models.base import GroupBase


class GroupReadBasic(GroupBase):
    id: uuid.UUID

class StudentRead(UserBase):
    id: uuid.UUID
    groups: list[GroupReadBasic]
    created_groups: list[GroupReadBasic]

class StudentReadWithoutGroups(UserBase):
    id: uuid.UUID

class StudentCreate(UserBase):
    pass
