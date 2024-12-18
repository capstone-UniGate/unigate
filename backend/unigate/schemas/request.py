import uuid

from unigate.enums import RequestStatus
from unigate.models.base import RequestBase
from unigate.schemas.student import StudentReadWithoutGroups


class RequestRead(RequestBase):
    id: uuid.UUID
    status: RequestStatus


class RequestReadWithStudent(RequestRead):
    id: uuid.UUID
    student: StudentReadWithoutGroups


class RequestCreate(RequestBase):
    pass
