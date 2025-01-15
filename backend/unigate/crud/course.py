import datetime

from sqlalchemy.sql import func
from sqlmodel import Session, select

from unigate.crud.base import CRUDBase
from unigate.models import Course, Group, Join
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

    def get_all_name_courses(self, *, session: Session) -> list[str]:
        return session.exec(select(self.model.name))

    def get_yearly_group_stats(
        self, session: Session, course_name: str
    ) -> dict[int, int]:
        """
        Get yearly group stats for a specific course.
        """
        statement = (
            select(func.extract("year", Group.date).label("year"), func.count(Group.id))
            .where(Group.course_name == course_name)
            .group_by("year")
            .order_by("year")
        )
        results = session.exec(statement).all()

        yearly_stats = {int(row.year): row.count for row in results}
        return yearly_stats

    def get_total_members(self, *, session: Session, course_name: str) -> int:
        statement = (
            select(func.count(func.distinct(Join.student_id)))
            .join(Group, Group.id == Join.group_id)
            .where(Group.course_name == course_name)
        )
        result = session.exec(statement).one_or_none()
        return result if result else 0


course = CRUDCourse(Course)
