import enum


class Role(str, enum.Enum):
    STUDENT = "S"
    PROFESSOR = "P"


class GroupType(str, enum.Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"


class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
