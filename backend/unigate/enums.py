import enum


class Mode(str, enum.Enum):
    TEST = "test"
    DEV = "dev"
    PROD = "prod"


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
    BLOCKED = "BLOCKED"
