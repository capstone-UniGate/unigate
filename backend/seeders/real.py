from datetime import datetime
from itertools import cycle

import pytz
from unigate import crud
from unigate.core.database import get_auth_session, get_session
from unigate.core.security import get_password_hash
from unigate.enums import GroupType
from unigate.models.course import Course
from unigate.models.exam import Exam
from unigate.models.teach import Teach
from unigate.schemas.auth import AuthUserCreate
from unigate.schemas.course import CourseCreate
from unigate.schemas.group import GroupCreate
from unigate.schemas.student import StudentCreate

students = [
    StudentCreate(
        number=4891185,
        email="s4891185@studenti.unige.it",
        name="Fabio",
        surname="Fontana",
    ),
    StudentCreate(
        number=4989646,
        email="s4989646@studenti.unige.it",
        name="Lorenzo",
        surname="Foschi",
    ),
    StudentCreate(
        number=5806782,
        email="s5806782@studenti.unige.it",
        name="Mimmo",
        surname="Torabi",
    ),
    StudentCreate(
        number=1234567,
        email="s1234567@studenti.unige.it",
        name="Test Name",
        surname="Test Surname",
    ),
    StudentCreate(
        number=6015033,
        email="s6015033@studenti.unige.it",
        name="Musse",
        surname="Gher",
    ),
    StudentCreate(
        number=4820312,
        email="s4820312@studenti.unige.it",
        name="Giovanni",
        surname="Bosi",
    ),
    StudentCreate(
        number=5475593,
        email="s5475593@studenti.unige.it",
        name="Forough",
        surname="Majidi",
    ),
    StudentCreate(
        number=4878744,
        email="s4878744@studenti.unige.it",
        name="Michele",
        surname="Frattini",
    ),
]

groups = [
    GroupCreate(
        name="Test Public Group",
        description="This is a test group",
        category="Test",
        type=GroupType.PUBLIC,
        course_name="Test Course",
        date=datetime(2025, 1, 1, tzinfo=pytz.utc),
        exam_date=datetime(2025, 1, 1, tzinfo=pytz.utc),
    ),
    GroupCreate(
        name="Test Private Group",
        description="This is a test group",
        category="Test",
        type=GroupType.PRIVATE,
        course_name="Test Course",
        date=datetime(2025, 1, 10, tzinfo=pytz.utc),
        exam_date=datetime(2025, 1, 10, tzinfo=pytz.utc),
    ),
]

courses = {
    CourseCreate(
        name="Test Course",
    ): [datetime(2025, 1, 1, tzinfo=pytz.utc), datetime(2025, 1, 25, tzinfo=pytz.utc)],
    CourseCreate(
        name="Binary Analysis and secure coding",
    ): [datetime(2025, 1, 8, tzinfo=pytz.utc), datetime(2025, 2, 10, tzinfo=pytz.utc)],
    CourseCreate(
        name="Capstone",
    ): [datetime(2025, 2, 3, tzinfo=pytz.utc), datetime(2025, 2, 17, tzinfo=pytz.utc)],
    CourseCreate(
        name="Decentralized Systems",
    ): [datetime(2025, 1, 14, tzinfo=pytz.utc), datetime(2025, 2, 13, tzinfo=pytz.utc)],
    CourseCreate(
        name="High Performance Computing",
    ): [datetime(2025, 1, 21, tzinfo=pytz.utc), datetime(2025, 2, 18, tzinfo=pytz.utc)],
    CourseCreate(
        name="Machine Learning",
    ): [datetime(2025, 1, 20, tzinfo=pytz.utc), datetime(2025, 2, 19, tzinfo=pytz.utc)],
    CourseCreate(
        name="Network Security",
    ): [datetime(2025, 1, 27, tzinfo=pytz.utc), datetime(2025, 2, 20, tzinfo=pytz.utc)],
    CourseCreate(
        name="Digital Forensics",
    ): [datetime(2025, 1, 28, tzinfo=pytz.utc), datetime(2025, 2, 21, tzinfo=pytz.utc)],
    CourseCreate(
        name="Virtualization and Cloud Computing",
    ): [datetime(2025, 2, 4, tzinfo=pytz.utc), datetime(2025, 2, 26, tzinfo=pytz.utc)],
    CourseCreate(
        name="Data Protection and Privacy",
    ): [datetime(2025, 2, 11, tzinfo=pytz.utc), datetime(2025, 2, 27, tzinfo=pytz.utc)],
}

users: list[AuthUserCreate] = []
for user in students:
    hashed_password = get_password_hash("testpassword")
    auth_user = AuthUserCreate.model_validate(
        user, update={"hashed_password": hashed_password}
    )
    users.append(auth_user)


def seed_auth() -> None:
    session = next(get_auth_session())
    created_courses: list[Course] = []
    for course, exam_dates in courses.items():
        created_course = Course(name=course.name)
        session.add(created_course)
        created_courses.append(created_course)
        for exam_date in exam_dates:
            session.add(Exam(course_id=created_course.id, date=exam_date))

    for i, user in enumerate(users):
        created_user = crud.auth_user.create(obj_in=user, session=session)
        if i % 3 == 0:
            for course in created_courses:
                session.add(
                    Teach(
                        professor_id=created_user.id,
                        course_id=course.id,
                    )
                )

    session.commit()


def seed_unigate() -> None:
    session = next(get_session())
    course_cycle = cycle(courses.items())

    for student in students:
        current_student = crud.student.create(obj_in=student, session=session)
        if student.number != 4820312:
            for group in groups:
                current_course, exam_dates = next(course_cycle)
                group = crud.group.create(
                    obj_in=group,
                    update={
                        "creator_id": current_student.id,
                        "name": f"{group.name} {current_student.number}",
                        "course_name": current_course.name,
                        "exam_date": exam_dates[0],
                    },
                    session=session,
                )
                group.students.append(current_student)
                group.super_students.append(current_student)
                session.add(group)
                session.commit()


if __name__ == "__main__":
    seed_auth()
    seed_unigate()
