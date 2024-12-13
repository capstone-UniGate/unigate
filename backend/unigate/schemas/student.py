import uuid

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


class StudentReadOnlyGroups(UserBase):
    groups: list[GroupReadBasic]
    created_groups: list[GroupReadBasic]
    super_groups: list[GroupReadBasic]
    blocked_groups: list[GroupReadBasic]


class StudentCreate(UserBase):
    pass
