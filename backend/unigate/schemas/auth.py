import uuid

from unigate.models.base import AuthUserBase, UserBase


class AuthUserCreate(AuthUserBase):
    pass


class UserReadWithoutCourses(UserBase):
    id: uuid.UUID
