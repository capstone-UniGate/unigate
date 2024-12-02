from typing import TypeVar

from sqlmodel import SQLModel
from unigate.core.database import get_auth_session
from unigate.models import User

from .base_crud import CRUDBase

ModelType = TypeVar("ModelType", bound=SQLModel)


class ReadUser(CRUDBase[User, User, User]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model
        self.db_session = next(get_auth_session())


user_read = ReadUser(User)
