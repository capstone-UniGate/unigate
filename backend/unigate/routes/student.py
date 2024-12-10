from fastapi import APIRouter, Depends
from sqlmodel import select

from unigate import crud
from unigate.models import Group, Student
from unigate.routes.deps import get_current_user
from unigate.schemas.group import GroupRead

router = APIRouter()


@router.get(
    "/groups",
    response_model=list[GroupRead],
)
def get_groups(
    current_user: Student = Depends(get_current_user(wanted_model=Student)),
) -> list[Group]:
    query = select(Group).where(Group.creator_id == current_user.id)
    return crud.group.get_multi(query=query)
