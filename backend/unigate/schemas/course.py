import datetime
import uuid

from pydantic import BaseModel

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


class GroupInfo(BaseModel):
    group_name: str
    students: list[str]


class ActiveCourseResponse(BaseModel):
    course_name: str
    total_students: int
    student_names: list[str]
    groups: list[GroupInfo]


class GroupDistributionInfo(BaseModel):
    group_name: str
    creation_date: datetime.datetime
    exam_date: datetime.date
    creator_name: str
    super_students: list[str]  # List of super student names


class CourseGroupDistributionResponse(BaseModel):
    course_name: str
    total_groups: int
    groups_info: list[GroupDistributionInfo]
