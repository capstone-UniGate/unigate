from fastapi import APIRouter, HTTPException, status

from unigate import crud
from unigate.core.database import AuthSessionDep, SessionDep
from unigate.models import Course
from unigate.schemas.course import CourseReadWithUsersAndExams

router = APIRouter()


@router.get(
    "",
    response_model=list[CourseReadWithUsersAndExams],
)
def get_courses(session: AuthSessionDep) -> list[Course]:
    return crud.course.get_all(session=session)


@router.get(
    "/get_info",
    response_model=dict[str, Course | int | None],
)
def get_info(
    session: SessionDep, auth_session: AuthSessionDep, course_name: str
) -> dict[str, Course | int | None]:
    result = {
        "course": crud.course.get_by_name(auth_session=auth_session, name=course_name),
        "count": crud.group.get_groups_num(session=session, course_name=course_name),
    }
    if not result["course"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return result
