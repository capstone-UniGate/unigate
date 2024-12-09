from sqlmodel import Session, select

from unigate.core.database import get_auth_session
from unigate.core.security import Role, verify_password
from unigate.models import AuthUser
from unigate.utils.auth import get_user

from .base_crud import CRUDBase


class ReadAuthUser(CRUDBase[AuthUser, AuthUser, AuthUser]):
    def __init__(self, model: type[AuthUser]) -> None:
        self.model = model
        self.db_session = next(get_auth_session())

    def get_db(self) -> Session:
        return next(get_auth_session())

    def get_by_number(
        self, *, number: int, db_session: Session | None = None
    ) -> AuthUser | None:
        db_session = db_session or super().get_db_session()
        statement = select(self.model).where(self.model.number == number)
        result = db_session.exec(statement)
        return result.one_or_none()

    def authenticate(self, *, number: int, role: str, password: str) -> AuthUser | None:
        unigate_user = get_user(number=number, role=Role(role), check_auth=False)
        if not unigate_user:
            return None
        auth_user = self.get_by_number(number=unigate_user.number)
        if not auth_user:
            return None
        if not verify_password(password, auth_user.hashed_password):
            return None
        return auth_user


auth_user = ReadAuthUser(AuthUser)
