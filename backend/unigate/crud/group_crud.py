import uuid
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from unigate.models import Group, GroupType, Student

from .base_crud import CRUDBase


class CRUDGroup(CRUDBase[Group, Group, Group]):
    def get_by_name(self, *, name: str) -> Group | None:
        db_session = self.get_db()
        statement = select(self.model).where(self.model.name == name)
        result = db_session.exec(statement)
        return result.first()

    def create_group(self, *, session: Session, group_data: Group) -> Group:

        # Validation: Check UUID format for group ID
        try:
            UUID(str(group_data.id))
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid UUID format for group ID."
            )

        # Validation 1: Check if a group with the same name already exists
        if self.get_by_name(name=group_data.name):
            raise HTTPException(
                status_code=400, detail="Group with this name already exists."
            )

        # Validation 2: Ensure the group type is valid (Public or Private)
        if group_data.type not in GroupType.__members__.values():
            raise HTTPException(
                status_code=400,
                detail="Invalid group type. Must be 'Public' or 'Private'.",
            )

        # Validation 3: Ensure the group ID is unique
        existing_group_id = session.exec(
            select(Group).where(Group.id == group_data.id)
        ).first()
        if existing_group_id:
            raise HTTPException(
                status_code=400, detail="A group with this ID already exists."
            )

        # Todo: it should be the authenticated user
        auth_user_id =uuid.uuid4()

        # Validation 4: Check if creator_id matches the authenticated user's ID
        if group_data.creator_id != auth_user_id:
            raise HTTPException(
                status_code=400, detail="Creator ID does not match the authenticated user."
            )

        try:
            # Attempt to add the new group
            session.add(group_data)
            session.commit()
            session.refresh(group_data)
            return group_data
        except IntegrityError:
            session.rollback()
            # Log the specific error message for more details
            print(f"IntegrityError: {str(e.orig)}")
            raise HTTPException(
                status_code=500, detail="An error occurred while creating the group."
            )


group_crud = CRUDGroup(Group)
