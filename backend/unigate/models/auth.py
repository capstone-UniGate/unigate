from sqlmodel import Field

from unigate.models.base import DBAuthBase, UUIDBase


class AuthUser(DBAuthBase, UUIDBase, table=True):
    __tablename__ = "users"  # type: ignore

    number: int = Field(unique=True, index=True, nullable=False, max_length=7)
    hashed_password: str = Field(nullable=False, index=True)
