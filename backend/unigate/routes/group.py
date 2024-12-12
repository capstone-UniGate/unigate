from fastapi import APIRouter, status, HTTPException

from unigate import crud
from unigate.models import Group, Student
from unigate.schemas.group import GroupRead, GroupCreate, GroupReadWithStudents
from unigate.schemas.student import StudentRead, StudentReadWithoutGroups
from unigate.routes.deps import StudentDep, GroupDep
from unigate.core.database import AuthSessionDep, SessionDep

import uuid

router = APIRouter()


@router.get(
    "",
    response_model=list[GroupReadWithStudents],
)
def get_groups(session: SessionDep) -> list[Group]:
    return crud.group.get_multi(session=session)


# @router.get(
#     "/{group_id}",
#     response_model=GroupRead,
# )
# def get_group(group_id: uuid.UUID) -> Group:
#     group = crud.group.get(id=group_id)
#     if not group:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found.")
#     return group

@router.post(
    "",
    response_model=GroupReadWithStudents,
)
def create_group(
    session: SessionDep,
    group: GroupCreate,
    current_user: StudentDep,
) -> Group:
    return crud.group.create(session=session, obj_in=group, update={"creator_id": current_user.id, "students": [current_user]})

# @router.get(
#     "/{group_id}/members",
#     response_model=list[StudentReadWithoutGroups],
# )
# def get_members(group_id: uuid.UUID) -> list[Student]:
#     # TODO: define the function to get the members of a group
#     # if the group is private, check if the current user is a member of the group
#     # if the group is public, return all the members of the group
#     group = crud.group.get(id=group_id)
#     if not group:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found.")
#     return group.students

@router.post(
    "/{group_id}/join",
    response_model=GroupReadWithStudents,
)
def join_group(
    session: SessionDep,
    group: GroupDep,
    current_user: StudentDep,
) -> Group:
    # TODO: define the function to join a group
    # if the group is private, create a join request
    # if the group is public, add the student to the group
    return crud.group.join(session=session, group=group, student=current_user)

# @router.get(
#     "/{group_id}/requests",
#     response_model=list[StudentRead],
# )
# def get_group_requests(group_id: uuid.UUID) -> list[StudentRead]:
#     # define the function to get the join requests for a group if the group is private
#     return crud.group.get_requests(id=group_id)
