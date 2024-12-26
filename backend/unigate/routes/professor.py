from fastapi import APIRouter, HTTPException, status

from unigate import crud
from unigate.core.database import AuthSessionDep
from unigate.models import Course
from unigate.schemas.course import (
    CourseReadWithUsersAndExams
)
from unigate.routes.deps import CurrProfessorDep

router = APIRouter()


@router.get(
    "/courses",
    response_model=list[CourseReadWithUsersAndExams],
)
def get_courses(current_professor: CurrProfessorDep) -> list[Course]:
    return current_professor.courses
