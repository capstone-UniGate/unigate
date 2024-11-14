from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from unigate.crud.group_crud import group_crud
from unigate.models import Group

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
