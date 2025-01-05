from datetime import datetime

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
]

groups = [
    GroupCreate(
        name="Test Public Group",
        description="This is a test group",
        category="Test",
        type=GroupType.PUBLIC,
        course_name="Test Course",
        date=datetime(2024, 1, 1, tzinfo=pytz.utc),
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
    ): [datetime(2025, 1, 1, tzinfo=pytz.utc), datetime(2025, 1, 10, tzinfo=pytz.utc)],
    CourseCreate(
        name="Capstone Project",
    ): [datetime(2023, 12, 1, tzinfo=pytz.utc), datetime(2024, 4, 14, tzinfo=pytz.utc)],
    CourseCreate(
        name="Decentralized Systems",
    ): [datetime(2024, 7, 3, tzinfo=pytz.utc), datetime(2023, 9, 14, tzinfo=pytz.utc)],
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
    for student in students:
        current_student = crud.student.create(obj_in=student, session=session)
        if student.number != 4820312:
            for group in groups:
                group = crud.group.create(
                    obj_in=group,
                    update={
                        "creator_id": current_student.id,
                        "name": f"{group.name} {current_student.number}",
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
