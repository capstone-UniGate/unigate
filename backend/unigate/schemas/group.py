import uuid

from unigate.models.group import GroupBase


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: uuid.UUID
