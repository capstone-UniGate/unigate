from sqlmodel import SQLModel  # type: ignore  # noqa: F401

from unigate.models.auth import AuthUser
from unigate.models.base import (
    AuthUserBase,
    DBAuthBase,
    DBUnigateBase,
    GroupBase,
    UserBase,
    UUIDBase,
)
from unigate.models.block import Block
from unigate.models.course import Course
from unigate.models.exam import Exam
from unigate.models.group import Group
from unigate.models.join import Join
from unigate.models.request import Request, RequestStatus
from unigate.models.student import Student
from unigate.models.super_student import SuperStudent

__all__ = [
    "AuthUser",
    "AuthUserBase",
    "Block",
    "Course",
    "DBAuthBase",
    "DBUnigateBase",
    "Exam",
    "Group",
    "GroupBase",
    "Join",
    "Request",
    "RequestStatus",
    "Student",
    "SuperStudent",
    "UUIDBase",
    "UserBase",
]
