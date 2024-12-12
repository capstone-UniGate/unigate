from fastapi import APIRouter, Depends
from sqlmodel import select

from unigate import crud
from unigate.core.database import SessionDep
from unigate.models import Group, Student
from unigate.routes.deps import get_current_user
from unigate.schemas.group import GroupReadWithStudents
from unigate.schemas.student import StudentRead

router = APIRouter()


@router.get("/me", response_model=StudentRead)
def get_me(
    current_user: Student = Depends(get_current_user(wanted_model=Student)),
) -> Student:
    return current_user


@router.get(
    "/groups",
    response_model=list[GroupReadWithStudents],
)
def get_groups(
    session: SessionDep,
    current_user: Student = Depends(get_current_user(wanted_model=Student)),
) -> list[Group]:
    query = select(Group).where(Group.creator_id == current_user.id)
    return crud.group.get_multi(session=session, query=query)
    # or
    # return current_user.groups + current_user.created_groups
