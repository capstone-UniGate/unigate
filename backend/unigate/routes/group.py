from fastapi import APIRouter

from unigate import crud
from unigate.core.database import SessionDep
from unigate.models import Group
from unigate.routes.deps import GroupDep, StudentDep
from unigate.schemas.group import GroupCreate, GroupReadWithStudents

router = APIRouter()


@router.get(
    "",
    response_model=list[GroupReadWithStudents],
)
def get_groups(session: SessionDep) -> list[Group]:
    return crud.group.get_multi(session=session)


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
    current_user: StudentDep,
) -> Group:
    return crud.group.create(
        session=session,
        obj_in=group,
        update={"creator_id": current_user.id, "students": [current_user]},
    )


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
