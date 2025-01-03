import uuid

from unigate.models.base import ExamBase


class ExamRead(ExamBase):
    id: uuid.UUID
