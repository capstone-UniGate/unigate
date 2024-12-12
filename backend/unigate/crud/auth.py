from sqlmodel import Session, select

from unigate.core.database import get_auth_session
from unigate.core.security import Role, verify_password
from unigate.models import AuthUser
from unigate.schemas.auth import AuthUserCreate
from unigate.utils.auth import get_user
from unigate.core.database import AuthSessionDep, SessionDep
from fastapi import Depends

from .base import CRUDBase


class ReadAuthUser(CRUDBase[AuthUser, AuthUserCreate, AuthUser]):
    def __init__(self, model: type[AuthUser]) -> None:
        self.model = model

    def get_by_number(
        self, *, number: int, session: Session
    ) -> AuthUser | None:
        statement = select(self.model).where(self.model.number == number)
        result = session.exec(statement)
        return result.one_or_none()

    def authenticate(self, *, number: int, role: str, password: str, session: Session, auth_session: Session) -> AuthUser | None:
        unigate_user = get_user(session=session, auth_session=auth_session, number=number, role=Role(role), check_auth=False)
        if not unigate_user:
            return None
        auth_user = self.get_by_number(number=unigate_user.number, session=auth_session)
        if not auth_user:
            return None
        if not verify_password(password, auth_user.hashed_password):
            return None
        return auth_user


auth_user = ReadAuthUser(AuthUser)
