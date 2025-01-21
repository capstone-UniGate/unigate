from sqlmodel import Session, select

from unigate.models import Student
from unigate.schemas.student import StudentCreate

from .base import CRUDBase


class CRUDStudent(CRUDBase[Student, StudentCreate, Student]):
    def get_by_number(self, *, number: int, session: Session) -> Student | None:
        statement = select(self.model).where(self.model.number == number)
        result = session.exec(statement)
        return result.one_or_none()


student = CRUDStudent(Student)
