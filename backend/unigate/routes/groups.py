from tokenize import group

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.exc import SQLAlchemyError
from unigate.crud.group_crud import group_crud
from unigate.crud.request_crud import request_crud
from unigate.models import Group,Request
from sqlmodel import Session, select

import uuid



router = APIRouter()


@router.get("/get", response_model=list[Group])
def get_groups() -> list[Group]:
    """
    Retrieve a list of all available groups.

    Args:
        session (Session): Database session to query the groups.

    Returns:
        List[Group]: A list of available groups.

    Raises:
        HTTPException: Raises a 500 error if the query fails.
    """
    try:
        return group_crud.get_multi()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Unable to load groups.")


@router.get("/{id}", response_model=Group)
def get_group(id: uuid.UUID) -> Group:
    group = group_crud.get(id=id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")
    else:
        return group


@router.get("/{group_id}/requests", response_model=list[Request])
def get_group_requests(group_id: uuid.UUID) -> list[Request]:

    group = group_crud.get(id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")

    requests = request_crud.get_all_requests_for_group(group_id=group_id)
    return requests
