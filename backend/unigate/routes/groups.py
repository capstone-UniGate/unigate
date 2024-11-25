import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from unigate.core.database import get_session
from unigate.crud.group_crud import group_crud
from unigate.crud.join_crud import join_crud
from unigate.crud.request_crud import request_crud
from unigate.crud.student_crud import student_crud
from unigate.models import Group, Request, Student

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
        raise HTTPException(status_code=500, detail="Unable to load groups.")


@router.post(
    "/create",
    response_model=Group,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Group successfully created", "model": Group},
        400: {"description": "Validation error while creating the group"},
        500: {"description": "An error occurred while creating the group"},
    },
)
def create_group(
    group_data: Group,
    session: Session = Depends(get_session),
) -> Group:
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
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the group.",
        )


@router.post(
    "/get_members",
    response_model=list[Student],
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "List of all students in the group",
            "model": list[Student],
        },
        400: {
            "description": "You cannot visualize members of a private group of which you are not part of"
        },
        500: {"description": "An error occurred while creating the group"},
    },
)
def get_memebrs(group_id: uuid.UUID, student_id: uuid.UUID | None) -> list[Student]:
    """
    Get a list of all memebers of a group

    Args:
        group_id (UUID): group's user ID
        student_id (UUID): student's user ID

    Returns:
        list[Students]: list of all students in that group

    Raises:
        HTTPException: Raises a 500 error if the query fails.
    """

    try:
        return student_crud.get_members(group_id=group_id, student_id=student_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post("/join_public_group", response_model=str)
def join_public_group(student_id: uuid.UUID, group_id: uuid.UUID) -> str:
    """
    Join a public group (if not already enrolled in another group for the same course).

    Args:
        student_id (UUID): student's user ID
        group_id (UUID): group's user ID

    Returns:
        bool: returns wether the join has failed ro not.

    Raises:
        HTTPException: Raises a 500 error if the query fails.
    """

    try:
        return join_crud.join_public_group(student_id, group_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post("/join_private_group", response_model=str)
def join_private_group(student_id: uuid.UUID, group_id: uuid.UUID) -> str:
    try:
        # Use the create_request method from request_crud to create a new join request
        request_crud.create_request(student_id, group_id)

        # Instead of returning the Request object, return a success message
        return "Join request submitted successfully."
    except SQLAlchemyError:
        # Generic SQLAlchemy error handling
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post("/get_student_groups", response_model=list[Group])
def get_student_groups(student_id: uuid.UUID) -> list[Group]:
    try:
        return join_crud.get_student_groups(student_id)
    except SQLAlchemyError:
        # Generic SQLAlchemy error handling
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get("/{id}", response_model=Group)
def get_group(id: uuid.UUID) -> Group:
    group = group_crud.get(id=id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")
    return group


@router.get("/{group_id}/requests", response_model=list[Request])
def get_group_requests(group_id: uuid.UUID) -> list[Request]:
    group = group_crud.get(id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")

    return request_crud.get_all_requests_for_group(group_id=group_id)
