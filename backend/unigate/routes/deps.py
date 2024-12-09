from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from unigate.core.config import settings
from unigate.core.security import Role
from unigate.models import Student
from unigate.schemas.token import TokenPayload
from unigate.utils.auth import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(token: TokenDep) -> Student:
    try:
        print(token)
        payload = jwt.decode(  # type: ignore
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        print(payload)
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError) as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    unigate_user = get_user(int(token_data.sub), Role(token_data.role))
    if not unigate_user:
        raise HTTPException(status_code=404, detail="User not found")
    return unigate_user


CurrentUser = Annotated[Student, Depends(get_current_user)]
