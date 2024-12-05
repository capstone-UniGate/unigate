from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from unigate.core.config import settings
from unigate.crud.auth_crud import user_read
from unigate.crud.student_crud import student
from unigate.models.auth import User
from unigate.utils.jwt import create_access_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    number: str | None = None


def get_user(number: int) -> User:
    student = student.get_by_number(number=number)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")

    return user_read.get_by_number(number=student.number)


def authenticate_user(number: int, password: str) -> User | bool:
    user = get_user(number)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


@router.post(
    "/login",
)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
        user = authenticate_user(int(form_data.username), form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token({"sub": user.number})
        return Token(access_token=access_token, token_type="bearer")  # noqa: S106
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unable to login.")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        number: str = payload.get("sub")
        if number is None:
            raise credentials_exception
        token_data = TokenData(number=number)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(token_data.number)
    if user is None:
        raise credentials_exception

    return user
