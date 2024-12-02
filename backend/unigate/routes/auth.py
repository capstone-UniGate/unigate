from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from unigate.crud.auth_crud import user_read
from unigate.crud.student_crud import student_crud
from unigate.utils.jwt import create_access_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post(
    "/login",
)
def login(number: int, password: str) -> Token:
    try:
        student = student_crud.get_by_number(number=number)
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found.")

        user = user_read.get(id=student.id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")

        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password.")

        # TODO: generate jwt token
        access_token = create_access_token({"sub": user.number})
        return Token(access_token=access_token, token_type="bearer")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Unable to load groups.")
