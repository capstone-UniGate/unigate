from typing import TypeVar

from sqlmodel import SQLModel, select

from unigate.models import User

from .base_crud import CRUDBase

ModelType = TypeVar("ModelType", bound=SQLModel)


class ReadUser(CRUDBase[User, User, User]):
    """def __init__(self, model: type[ModelType]) -> None:
        self.model = model
        self.db_session = next(get_auth_session())

    def get_db(self) -> Session:
        return next(get_auth_session())"""

    def get_by_number(self, *, number: int) -> ModelType | None:
        query = select(self.model).where(self.model.number == number)
        response = self.db_session.exec(query)
        return response.one_or_none()

    def get(self, *, id: int | str) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        response = self.db_session.exec(query)
        return response.one_or_none()


user_read = ReadUser(User)
