import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel  # type: ignore


class UUIDBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class UserBase(UUIDBase):
    number: int = Field(unique=True, index=True, nullable=False, max_length=7)
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    name: str = Field(nullable=False)
    surname: str = Field(nullable=True)
