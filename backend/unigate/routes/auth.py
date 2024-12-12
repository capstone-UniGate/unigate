from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from unigate import crud
from unigate.core.security import Role, create_access_token
from unigate.schemas.token import Token
from unigate.core.database import AuthSessionDep, SessionDep


router = APIRouter()


def get_role_and_number(username: str) -> tuple[str, int]:
    if len(username) < 2:
        raise HTTPException(status_code=401, detail="Invalid username")
    role = username[0]
    number = int(username[1:])
    return role, number


@router.post(
    "/login",
)
def login(session: SessionDep, auth_session: AuthSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
        role, number = get_role_and_number(form_data.username)
        user = crud.auth_user.authenticate(
            session=session, auth_session=auth_session, number=number, role=role, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token = create_access_token(subject_number=user.number, role=Role(role))
        return Token(access_token=access_token, token_type="bearer")  # noqa: S106
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unable to login.")
