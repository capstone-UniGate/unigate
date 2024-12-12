from collections.abc import Callable
from typing import Annotated
import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from pydantic import ValidationError

from unigate import crud
from unigate.core.config import settings
from unigate.enums import Role
from unigate.models import Student
from unigate.models.group import Group
from unigate.schemas.token import TokenPayload
from unigate.utils.auth import get_user
from unigate.core.database import get_session, get_auth_session
from unigate.core.database import AuthSessionDep, SessionDep

from sqlmodel import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(
    wanted_model: type[Student] | None = None,
) -> Callable[[SessionDep, AuthSessionDep, TokenDep], Student]:
    def get_current_user_aux(session: SessionDep, auth_session: AuthSessionDep, token: TokenDep) -> Student:
        try:
            payload = jwt.decode(  # type: ignore
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except (jwt.InvalidTokenError, ValidationError) as e:
            logger.error(f"Invalid token: {e}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        unigate_user = get_user(session=session, auth_session=auth_session, number=int(token_data.sub), role=Role(token_data.role))
        if not unigate_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if wanted_model and not isinstance(unigate_user, wanted_model):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User is not a {wanted_model.__name__}",
            )
        return unigate_user

    return get_current_user_aux


StudentDep = Annotated[Student, Depends(get_current_user(wanted_model=Student))]


def get_group(
    session: SessionDep,
    group_id: uuid.UUID,
) -> Group:
    group = crud.group.get(id=group_id, session=session)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found.")
    return group


GroupDep = Annotated[Group, Depends(get_group)]
