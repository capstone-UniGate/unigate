from sqlmodel import select
from unigate.models import Student, Join, Group, GroupType
from unigate.crud.group_crud import group_crud

from .base_crud import CRUDBase

import uuid


class CRUDStudent(CRUDBase[Student, Student, Student]):
    def get_by_name(self, *, name: str) -> Student | None:
        db_session = self.get_db()
        statement = select(self.model).where(self.model.name == name)
        result = db_session.exec(statement)
        return result.one_or_none()
    
    def get_members(self, *, group_id:uuid.UUID, student_id:uuid.UUID | None)->list[Student]:
        group = group_crud.get(id=group_id)
        if(group.type == GroupType.PRIVATE and not self.check_membership(group_id=group_id, student_id=student_id)):
            return []
        statement = (
                select(self.model)
                .join(Join)
                .where(Join.group_id == group_id)
            )
        return self.get_multi(query=statement)
    
    def check_membership(self, *, group_id: uuid.UUID, student_id: uuid.UUID | None) -> bool:
        if student_id is None:
            return False
        db_session = self.get_db()
        statement = (select(self.model)
                     .join(Join)
                     .where(Group.id == group_id)
                     .where(self.model.id == student_id)
        )
        result = db_session.exec(statement)
        return result.one_or_none() is not None


student_crud = CRUDStudent(Student)
