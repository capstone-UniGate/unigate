from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    number: int = Field(primary_key=True, index=True)
    hashed_password: str
