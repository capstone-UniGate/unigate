import datetime

from sqlmodel import Session, select

from unigate.crud.base import CRUDBase
from unigate.models import Course
from unigate.schemas.course import CourseCreate


class CRUDCourse(CRUDBase[Course, CourseCreate, Course]):
    def __init__(self, model: type[Course]) -> None:
        self.model = model

    def get_by_name(self, *, name: str, auth_session: Session) -> Course | None:
        statement = select(self.model).where(self.model.name == name)
        result = auth_session.exec(statement)
        return result.one_or_none()

    def get_by_name_and_exam(
        self, *, name: str, exam_date: datetime.date | None, auth_session: Session
    ) -> Course | None:
        statement = select(self.model).where(self.model.name == name)
        result = auth_session.exec(statement)
        course = result.one_or_none()
        if course is None:
            return None
        if exam_date is None:
            return course
        for exam in course.exams:
            if exam.date == exam_date:
                return course
        return None


course = CRUDCourse(Course)
