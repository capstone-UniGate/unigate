from unigate import crud
from unigate.core.security import Role
from unigate.models import Student


def get_user(number: int, role: Role, *, check_auth: bool = True) -> Student | None:
    if check_auth:
        auth_user = crud.auth_user.get_by_number(number=number)
        if auth_user is None:
            return None

    if role == Role.STUDENT:
        return crud.student.get_by_number(number=number)
    # elif role == Role.PROFESSOR:
    #     return crud.professor.get_by_number(number=number)

    return None
