import random
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
        number=1234567,
        email="s1234567@studenti.unige.it",
        name="Test Name",
        surname="Test Surname",
    ),
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

professors = [
    AuthUserCreate(
        number=0,
        email="test@unige.it",
        name="Test Name",
        surname="Test Surname",
        hashed_password=get_password_hash("testpassword"),
    ),
    AuthUserCreate(
        number=1000000,
        email="marina.ribaudo@unige.it",
        name="Marina",
        surname="Ribaudo",
        hashed_password=get_password_hash("testpassword"),
    ),
    AuthUserCreate(
        number=2000000,
        email="maura.cerioli@unige.it",
        name="Maura",
        surname="Cerioli",
        hashed_password=get_password_hash("testpassword"),
    ),
    AuthUserCreate(
        number=3000000,
        email="matteo.dellamico@unige.it",
        name="Matteo",
        surname="Dell'Amico",
        hashed_password=get_password_hash("testpassword"),
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
        date=datetime(2025, 1, 1, tzinfo=pytz.utc),
        exam_date=datetime(2025, 1, 1, tzinfo=pytz.utc),
    ),
]

courses = {
    "Test Course": {
        "course": CourseCreate(name="Test Course"),
        "professors": [professors[0]],
        "exam_dates": [datetime(2025, 1, 1, tzinfo=pytz.utc)],
    },
    "Capstone": {
        "course": CourseCreate(name="Capstone"),
        "professors": [professors[1], professors[2]],
        "exam_dates": [],
    },
    "Distributed Systems": {
        "course": CourseCreate(name="Distributed Systems"),
        "professors": [professors[1], professors[3]],
        "exam_dates": [],
    },
}


# Generate random exam dates for January, February, June, July, and September
def generate_exam_dates():
    months = [1, 2, 6, 7, 9]
    return [
        datetime(2025, month, random.randint(1, 28), tzinfo=pytz.utc)
        for month in months
    ]


for course_name, details in courses.items():
    if course_name != "Test Course":
        details["exam_dates"] = generate_exam_dates()


users = professors + [
    AuthUserCreate.model_validate(
        student,
        update={"hashed_password": get_password_hash("testpassword")},
    )
    for student in students
]

test_student = students[0]


def seed_auth() -> None:
    session = next(get_auth_session())
    created_courses = {}

    for course_name, details in courses.items():
        created_course = Course(name=details["course"].name)
        session.add(created_course)
        created_courses[course_name] = created_course

        for exam_date in details["exam_dates"]:
            session.add(Exam(course_id=created_course.id, date=exam_date))

    for user in users:
        created_user = crud.auth_user.create(obj_in=user, session=session)
        if user in professors:
            for course_name, details in courses.items():
                if user in details["professors"]:
                    session.add(
                        Teach(
                            professor_id=created_user.id,
                            course_id=created_courses[course_name].id,
                        )
                    )
    session.commit()


def seed_unigate() -> None:
    session = next(get_session())

    for student in students:
        current_student = crud.student.create(obj_in=student, session=session)
        for group in groups:
            current_group = crud.group.create(
                obj_in=group,
                update={
                    "creator_id": current_student.id,
                    "name": f"Test {student.number} {group.type.value}",
                    "course_name": group.course_name,
                    "exam_date": group.exam_date,
                },
                session=session,
            )
            current_group.students.append(current_student)
            current_group.super_students.append(current_student)
            session.add(current_group)
            session.commit()


if __name__ == "__main__":
    seed_auth()
    seed_unigate()
