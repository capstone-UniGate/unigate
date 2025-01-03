import uuid

from unigate.models.base import CourseBase
from unigate.schemas.auth import UserReadWithoutCourses
from unigate.schemas.exam import ExamRead


class CourseRead(CourseBase):
    id: uuid.UUID


class CourseCreate(CourseBase):
    def __hash__(self) -> int:
        return hash(self.name)


class CourseReadWithUsersAndExams(CourseRead):
    professors: list[UserReadWithoutCourses]
    exams: list[ExamRead]
