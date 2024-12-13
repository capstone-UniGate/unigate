import uuid

from unigate.models.base import RequestBase
from unigate.schemas.student import StudentReadWithoutGroups


class RequestRead(RequestBase):
    id: uuid.UUID


class RequestReadWithStudent(RequestRead):
    id: uuid.UUID
    student: StudentReadWithoutGroups


class RequestCreate(RequestBase):
    pass
