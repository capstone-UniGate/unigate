from fastapi import APIRouter

from unigate.models import Course
from unigate.routes.deps import CurrProfessorDep
from unigate.schemas.course import CourseReadWithUsersAndExams

router = APIRouter()


@router.get(
    "/courses",
    response_model=list[CourseReadWithUsersAndExams],
)
def get_courses(current_professor: CurrProfessorDep) -> list[Course]:
    return current_professor.courses
