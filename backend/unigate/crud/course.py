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
    ) -> dict[int, dict[str, int]]:
        """
        Get yearly group stats for a specific course.
        Includes totalGroups and totalMembers per year.
        """
        statement = (
            select(
                func.extract("year", Group.date).label("year"),
                func.count(Group.id).label("totalGroups"),  # Total number of groups
                func.count(Join.student_id).label(
                    "totalMembers"
                ),  # Total member occurrences
            )
            .join(Join, Join.group_id == Group.id)  # Join groups with joins table
            .where(Group.course_name == course_name)  # Filter by course name
            .group_by("year")  # Group by year
            .order_by("year")  # Order by year
        )

        results = session.exec(statement).all()

        yearly_stats = {
            int(row.year): {
                "totalGroups": row.totalGroups,
                "totalMembers": row.totalMembers,
            }
            for row in results
        }
        return yearly_stats


course = CRUDCourse(Course)
