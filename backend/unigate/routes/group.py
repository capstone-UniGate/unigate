from fastapi import APIRouter, HTTPException, status

from unigate import crud
from unigate.core.database import SessionDep
from unigate.enums import GroupType
from unigate.models import Group, Request
from unigate.routes.deps import CurrStudentDep, GroupDep, RequestDep, StudentDep
from unigate.schemas.group import (
    GroupCreate,
    GroupReadOnlyStudents,
    GroupReadWithStudents,
)
from unigate.schemas.request import RequestRead

router = APIRouter()


@router.get(
    "",
    response_model=list[GroupReadWithStudents],
)
def get_groups(session: SessionDep) -> list[Group]:
    return crud.group.get_all(session=session)


@router.get(
    "/{group_id}",
    response_model=GroupReadWithStudents,
)
def get_group(group: GroupDep) -> Group:
    return group


@router.post(
    "",
    response_model=GroupReadWithStudents,
)
def create_group(
    session: SessionDep,
    group: GroupCreate,
    current_user: CurrStudentDep,
) -> Group:
    return crud.group.create(
        session=session,
        obj_in=group,
        update={
            "creator_id": current_user.id,
            "students": [current_user],
            "super_students": [current_user],
        },
    )


@router.post(
    "/{group_id}/join",
    response_model=GroupReadWithStudents,
)
def join_group(
    session: SessionDep,
    group: GroupDep,
    current_user: CurrStudentDep,
) -> Group:
    if group.type == GroupType.PRIVATE:
        return crud.group.create_request(
            session=session, group=group, student=current_user
        )
    return crud.group.join(session=session, group=group, student=current_user)


@router.post(
    "/{group_id}/leave",
    response_model=GroupReadWithStudents,
)
def leave_group(
    session: SessionDep,
    group: GroupDep,
    current_user: CurrStudentDep,
) -> Group:
    return crud.group.leave(session=session, group=group, student=current_user)


@router.get(
    "/{group_id}/students",
    response_model=GroupReadOnlyStudents,
)
def get_group_students(
    group: GroupDep,
) -> Group:
    return group


@router.get(
    "/{group_id}/requests",
    response_model=list[RequestRead],
)
def get_group_requests(
    group: GroupDep,
    current_user: CurrStudentDep,
) -> list[Request]:
    if current_user not in group.super_students:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a super student of this group",
        )
    return group.requests


@router.post(
    "/{group_id}/requests/{request_id}/approve",
    response_model=RequestRead,
)
def accept_group_request(
    session: SessionDep,
    group: GroupDep,
    request: RequestDep,
    current_user: CurrStudentDep,
) -> Request:
    if current_user not in group.super_students:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a super student of this group",
        )
    return crud.group.approve_request(session=session, request=request)


@router.post(
    "/{group_id}/requests/{request_id}/reject",
    response_model=RequestRead,
)
def reject_group_requesr(
    session: SessionDep,
    group: GroupDep,
    request: RequestDep,
    current_user: CurrStudentDep,
) -> Request:
    if current_user not in group.super_students:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a super student of this group",
        )
    return crud.group.reject_request(session=session, request=request)


@router.post(
    "/{group_id}/requests/{request_id}/block",
    response_model=RequestRead,
)
def block_group_request(
    session: SessionDep,
    group: GroupDep,
    request: RequestDep,
    current_user: CurrStudentDep,
) -> Request:
    if current_user not in group.super_students:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a super student of this group",
        )
    return crud.group.block_request(session=session, request=request)


@router.post(
    "/{group_id}/students/{student_id}/block",
    response_model=GroupReadWithStudents,
)
def block_user(
    session: SessionDep,
    group: GroupDep,
    student: StudentDep,
    current_user: CurrStudentDep,
) -> Group:
    if current_user not in group.super_students:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a super student of this group",
        )
    return crud.group.block_user(session=session, group=group, student=student)


@router.post(
    "/{group_id}/students/{student_id}/unblock",
    response_model=GroupReadWithStudents,
)
def unblock_user(
    session: SessionDep,
    group: GroupDep,
    student: StudentDep,
    current_user: CurrStudentDep,
) -> Group:
    if current_user not in group.super_students:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a super student of this group",
        )
    return crud.group.unblock_user(session=session, group=group, student=student)
