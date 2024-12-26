from fastapi import APIRouter, HTTPException, status

from unigate import crud
from unigate.core.database import AuthSessionDep
from unigate.models import Course
from unigate.schemas.course import (
    CourseReadWithUsersAndExams
)

router = APIRouter()


@router.get(
    "",
    response_model=list[CourseReadWithUsersAndExams],
)
def get_courses(session: AuthSessionDep) -> list[Course]:
    return crud.course.get_all(session=session)
