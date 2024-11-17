from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from unigate.core.database import get_session
from unigate.crud.group_crud import group_crud
from unigate.models import Group

router = APIRouter()


# routes/groups.py
@router.get(
    "/get",
    response_model=list[Group],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "A list of all available groups", "model": list[Group]},
        500: {"description": "Unable to load groups due to a server error"},
    },
)
def get_groups() -> list[Group]:
    """
    Retrieve a list of all available groups.

    This endpoint fetches all group entries from the database.

    Returns:
    - **200 OK**: A list of all groups, each represented by a `Group` model.
    - **500 Internal Server Error**: An error occurred while attempting to load the groups.
    """
    try:
        return group_crud.get_multi()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load groups.",
        )


@router.post(
    "/create",
    response_model=Group,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Group successfully created", "model": Group},
        400: {"description": "Group with this name already exists"},
        500: {"description": "An error occurred while creating the group"},
    },
)
def create_group(
    group_data: Group,
    session: Session = Depends(get_session),
) -> None:
    """
    Creates a new group in the system.

    - **name**: The unique name of the group.
    - **description**: (Optional) A brief description of the group's purpose.
    - **category**: (Optional) The category this group belongs to.
    - **type**: The type of group, either "Public" or "Private".
    - **creator_id**: The ID of the user creating the group.

    This endpoint checks for duplicate group names before creating a new group.
    """
    try:
        return group_crud.create_group(session=session, group_data=group_data)

    except HTTPException:
        raise  # Re-raise any HTTPExceptions for client handling
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the group.",
        )
