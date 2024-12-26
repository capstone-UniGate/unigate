from sqlmodel import Session

from unigate import crud
from unigate.core.security import Role
from unigate.models import AuthUser, Student


def get_user(
    session: Session,
    auth_session: Session,
    number: int,
    role: Role,
    # *,
    # check_auth: bool = True,
) -> Student | AuthUser | None:
    # if check_auth:
    auth_user = crud.auth_user.get_by_number(session=auth_session, number=number)
    if auth_user is None:
        return None

    if role == Role.STUDENT:
        return crud.student.get_by_number(session=session, number=number)
    # elif role == Role.PROFESSOR:
    # auth_user is a professor
    return auth_user
