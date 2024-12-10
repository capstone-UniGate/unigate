import uuid

from sqlmodel import select

from unigate.models import SuperStudent

from .base import CRUDBase


class SuperStudentCRUD(CRUDBase[SuperStudent, SuperStudent, SuperStudent]):
    def get_by_group_id(self, group_id: uuid.UUID) -> SuperStudent | None:
        db_session = self.get_db_session()
        return db_session.exec(
            select(SuperStudent).where(SuperStudent.group_id == group_id)
        ).first()


super_student_crud = SuperStudentCRUD(SuperStudent)
