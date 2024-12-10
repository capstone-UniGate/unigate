import uuid

from pydantic import EmailStr
from sqlalchemy.orm import registry
from sqlmodel import Column, Enum, Field, SQLModel  # type: ignore

from unigate.enums import GroupType


class DBAuthBase(SQLModel, registry=registry()):
    pass


class DBUnigateBase(SQLModel, registry=registry()):
    pass


class UUIDBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class UserBase(SQLModel):
    number: int = Field(unique=True, index=True, nullable=False, ge=0, le=9999999)
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    name: str = Field(nullable=False)
    surname: str = Field(nullable=True)


class AuthUserBase(UserBase):
    hashed_password: str = Field(nullable=False, index=True)


class GroupBase(SQLModel):
    name: str
    description: str | None = None
    category: str | None = None
    type: GroupType = Field(sa_column=Column(Enum(GroupType, name="group_type")))
