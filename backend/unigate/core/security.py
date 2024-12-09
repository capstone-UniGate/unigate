import enum
from datetime import UTC, datetime, timedelta

import jwt
from passlib.context import CryptContext

from unigate.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


class Role(enum.Enum):
    STUDENT = "S"
    PROFESSOR = "P"


def create_access_token(
    subject_number: int, role: Role, expires_delta: timedelta | None = None
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)
    expire = datetime.now(UTC) + expires_delta
    to_encode: dict[str, datetime | str] = {
        "exp": expire,
        "sub": str(subject_number),
        "role": role.value,
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)  # type: ignore


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
