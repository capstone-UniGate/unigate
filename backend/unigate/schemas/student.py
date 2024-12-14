import uuid

from pydantic import BaseModel

from unigate.models.base import GroupBase, UserBase


class GroupReadBasic(GroupBase):
    id: uuid.UUID


class StudentRead(UserBase):
    id: uuid.UUID
    groups: list[GroupReadBasic]
    created_groups: list[GroupReadBasic]
    super_groups: list[GroupReadBasic]


class StudentReadWithoutGroups(UserBase):
    id: uuid.UUID


class StudentReadOnlyGroups(BaseModel):
    groups: list[GroupReadBasic]
    created_groups: list[GroupReadBasic]
    super_groups: list[GroupReadBasic]
    blocked_groups: list[GroupReadBasic]


class StudentCreate(UserBase):
    pass
