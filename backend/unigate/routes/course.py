from fastapi import APIRouter, HTTPException, status

from unigate import crud
from unigate.core.database import AuthSessionDep, SessionDep
from unigate.models import Course, Group
from unigate.schemas.course import (
    ActiveCourseResponse,
    CourseGroupDistributionResponse,
    CourseReadWithUsersAndExams,
    GroupDistributionInfo,
)
from unigate.schemas.group import (
    GroupReadWithStudents,
    NumberMembersOfGroups,
    NumberOfGroupsResponse,
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


@router.get("/{course_name}/active", response_model=ActiveCourseResponse)
def check_active_course(
    session: SessionDep, course_name: str, exam_date: str
) -> ActiveCourseResponse:
    groups = crud.group.get_groups_exam(
        session=session, course_name=course_name, date=exam_date
    )
    all_students = set()
    student_names = []
    for group in groups:
        for student in group.students:
            if student.id not in all_students:
                all_students.add(student.id)
                student_names.append(f"{student.name} {student.surname or ''}")
    return ActiveCourseResponse(
        course_name=course_name,
        total_students=len(all_students),
        student_names=student_names,
    )


@router.get(
    "/{course_name}/distribution", response_model=CourseGroupDistributionResponse
)
def get_group_distribution(
    session: SessionDep,
    course_name: str,
) -> CourseGroupDistributionResponse:
    groups = crud.group.get_groups_course(session=session, course_name=course_name)
    groups_info = [
        GroupDistributionInfo(
            group_name=group.name,
            creation_date=group.date,
            exam_date=group.exam_date,
            creator_name=f"{group.creator.name} {group.creator.surname or ''}",
            super_students=[
                f"{student.name} {student.surname or ''}"
                for student in group.super_students
            ],
        )
        for group in groups
    ]
    groups_info.sort(key=lambda x: x.creation_date)
    return CourseGroupDistributionResponse(
        course_name=course_name, total_groups=len(groups_info), groups_info=groups_info
    )


@router.get(
    "/{course_name}/number_of_groups",
    response_model=NumberOfGroupsResponse,
)
def number_of_groups(
    session: SessionDep, auth_session: AuthSessionDep, course_name: str
) -> NumberOfGroupsResponse:
    course = crud.course.get_by_name(auth_session=auth_session, name=course_name)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return crud.group.number_of_groups(session=session, course_name=course_name)


@router.get(
    "/{course_name}/average_members",
    response_model=NumberMembersOfGroups,
)
def average_members(
    session: SessionDep, auth_session: AuthSessionDep, course_name: str
) -> NumberMembersOfGroups:
    course = crud.course.get_by_name(auth_session=auth_session, name=course_name)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return crud.group.average_members(session=session, course_name=course_name)
