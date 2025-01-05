from fastapi import APIRouter, HTTPException, status

from unigate import crud
from unigate.core.database import AuthSessionDep, SessionDep
from unigate.models import Course, Group
from unigate.schemas.course import CourseReadWithUsersAndExams
from unigate.schemas.group import (
    GroupReadWithStudents, NumberOfGroupsResponse, NumberMembersOfGroups
)

router = APIRouter()


@router.get(
    "",
    response_model=list[CourseReadWithUsersAndExams],
)
def get_courses(session: AuthSessionDep) -> list[Course]:
    return crud.course.get_all(session=session)


@router.get(
    "/get_group_number",
    response_model=dict[str, Course | int | None],
)
def get_group_number(
    session: SessionDep, auth_session: AuthSessionDep, course_name: str
) -> dict[str, Course | int | None]:
    result = {
        "course": crud.course.get_by_name(auth_session=auth_session, name=course_name),
        "count": len(
            crud.group.get_groups_course(session=session, course_name=course_name)
        ),
    }
    if not result["course"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return result


@router.get(
    "/get_groups",
    response_model=list[GroupReadWithStudents],
)
def get_groups(
    session: SessionDep, auth_session: AuthSessionDep, course_name: str
) -> list[Group]:
    course = crud.course.get_by_name(auth_session=auth_session, name=course_name)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return crud.group.get_groups_course(session=session, course_name=course_name)


@router.get(
    "/get_groups_exams",
    response_model=list[GroupReadWithStudents],
)
def get_groups_exams(
    session: SessionDep, auth_session: AuthSessionDep, course_name: str, date: str
) -> list[Group]:
    course = crud.course.get_by_name(auth_session=auth_session, name=course_name)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return crud.group.get_groups_exam(
        session=session, course_name=course_name, date=date
    )

@router.get(
    "/{course_name}/number_of_groups",
    response_model= NumberOfGroupsResponse,
)
def number_of_groups(
    session: SessionDep, auth_session: AuthSessionDep, course_name: str) -> NumberOfGroupsResponse:
    course = crud.course.get_by_name(auth_session=auth_session, name=course_name)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return crud.group.number_of_groups(session=session, course_name=course_name)

@router.get(
    "/{course_name}/average_members",
    response_model= NumberMembersOfGroups,
)
def average_members(
    session: SessionDep, auth_session: AuthSessionDep, course_name: str) -> NumberMembersOfGroups:
    course = crud.course.get_by_name(auth_session=auth_session, name=course_name)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return crud.group.average_members(session=session, course_name=course_name)