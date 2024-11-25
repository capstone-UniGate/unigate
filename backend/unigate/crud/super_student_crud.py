import uuid

from unigate.models import SuperStudent
from sqlmodel import Session

from .base_crud import CRUDBase

class SuperStudentCRUD(CRUDBase[SuperStudent,SuperStudent,SuperStudent]):

    def get_by_group_id(self, session: Session, group_id: uuid.UUID) -> SuperStudent:
        return session.query(SuperStudent).filter(SuperStudent.group_id == group_id).first()
