from sqlmodel import Session, select

from unigate.models import Student
from unigate.schemas.student import StudentCreate

from .base import CRUDBase


class CRUDStudent(CRUDBase[Student, StudentCreate, Student]):
    def get_by_number(
        self, *, number: int, db_session: Session | None = None
    ) -> Student | None:
        db_session = db_session or super().get_db_session()
        statement = select(self.model).where(self.model.number == number)
        result = db_session.exec(statement)
        return result.one_or_none()

    # def get_members(
    #     self, *, group_id: uuid.UUID, student_id: uuid.UUID | None
    # ) -> list[Student]:
    #     group = group.get(id=group_id)
    #     if group.type == GroupType.PRIVATE and not self.check_membership(
    #         group_id=group_id, student_id=student_id
    #     ):
    #         return []
    #     statement = select(self.model).join(Join).where(Join.group_id == group_id)
    #     return self.get_multi(query=statement)

    # def check_membership(
    #     self, *, group_id: uuid.UUID, student_id: uuid.UUID | None
    # ) -> bool:
    #     if student_id is None:
    #         return False
    #     db_session = self.get_db_session()
    #     statement = (
    #         select(self.model)
    #         .join(Join)
    #         .where(Group.id == group_id)
    #         .where(self.model.id == student_id)
    #     )
    #     result = db_session.exec(statement)
    #     return result.one_or_none() is not None


student = CRUDStudent(Student)
