from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from unigate.core.config import settings
from unigate.enums import Role


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


def verify_password(plain_password: str | bytes, hashed_password: str | bytes) -> bool:
    if isinstance(plain_password, str):
        plain_password = plain_password.encode()
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode()

    return bcrypt.checkpw(plain_password, hashed_password)


def get_password_hash(plain_password: str | bytes) -> str:
    if isinstance(plain_password, str):
        plain_password = plain_password.encode()

    return bcrypt.hashpw(plain_password, bcrypt.gensalt()).decode()
