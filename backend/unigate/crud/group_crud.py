# crud/group_crud.py
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from unigate.models import Group

from .base_crud import CRUDBase


class CRUDGroup(CRUDBase[Group, Group, Group]):
    def get_by_name(self, *, name: str) -> Group | None:
        db_session = self.get_db()
        statement = select(self.model).where(self.model.name == name)
        result = db_session.exec(statement)
        return result.first()

    def create_group(self, *, session: Session, group_data: Group) -> Group:
        # TODO: validate by type and not by simply name
        if self.get_by_name(name=group_data.name):
            raise HTTPException(
                status_code=400, detail="Group with this name already exists."
            )

        try:
            session.add(group_data)
            session.commit()
            session.refresh(group_data)
            return group_data
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=500, detail="An error occurred while creating the group."
            )


group_crud = CRUDGroup(Group)
