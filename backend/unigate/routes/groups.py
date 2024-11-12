from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from unigate.core import get_session
from unigate.models import Group

router = APIRouter()


@router.get("/getall", response_model=list[Group])
async def get_groups(session: Session = Depends(get_session)) -> list[Group]:
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
        statement = select(Group)
        return session.exec(statement).all()
    except SQLAlchemyError:
        # Log the error message if a logging system is available
        raise HTTPException(status_code=500, detail="Unable to load groups.")
