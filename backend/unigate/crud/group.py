from sqlmodel import Session, select

from unigate.crud.base import CRUDBase
from unigate.models import Group
from unigate.models.student import Student
from unigate.schemas.group import GroupCreate
from fastapi import Depends
from unigate.core.database import get_session


class CRUDGroup(CRUDBase[Group, GroupCreate, Group]):
    def get_by_name(
        self, *, name: str, db_session: Session = Depends(get_session)
    ) -> Group | None:
        statement = select(self.model).where(self.model.name == name)
        result = db_session.exec(statement)
        return result.one_or_none()

    def join(
        self, *, group: Group, student: Student, session: Session
    ) -> Group:
        group.students.append(student)
        session.add(group)
        session.commit()
        session.refresh(group)
        return group


group = CRUDGroup(Group)
