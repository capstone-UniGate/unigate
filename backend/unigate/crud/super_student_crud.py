import uuid

from unigate.models import SuperStudent

from .base_crud import CRUDBase


class SuperStudentCRUD(CRUDBase[SuperStudent, SuperStudent, SuperStudent]):
    def get_by_group_id(self, group_id: uuid.UUID) -> SuperStudent:
        db_session = self.get_db()
        return (
            db_session.query(SuperStudent)
            .filter(SuperStudent.group_id == group_id)
            .first()
        )


super_student_crud = SuperStudentCRUD(SuperStudent)
