import random
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

test_student = StudentCreate(
    number=1234567,
    email="s1234567@studenti.unige.it",
    name="Test Name",
    surname="Test Surname",
)

professors = [
    AuthUserCreate(
        number=101810,
        email="marina.ribaudo@unige.it",
        name="Marina",
        surname="Ribaudo",
        hashed_password=get_password_hash("profpassword"),
    ),
    AuthUserCreate(
        number=101811,
        email="maura.cerioli@unige.it",
        name="Maura",
        surname="Cerioli",
        hashed_password=get_password_hash("profpassword"),
    ),
    AuthUserCreate(
        number=3333333,
        email="matteo@unige.it",
        name="Matteo",
        surname="Dell Amico",
        hashed_password=get_password_hash("profpassword"),
    ),
]

groups = [
    GroupCreate(
        name="Test Student Group",
        description="Group for testing purposes",
        category="Test",
        type=GroupType.PUBLIC,
        course_name="Test Course",
        date=datetime(2025, 1, 1, tzinfo=pytz.utc),
        exam_date=datetime(2025, 1, 15, tzinfo=pytz.utc),
    ),
]

courses = {
    "Capstone": {
        "course": CourseCreate(name="Capstone"),
        "professors": [professors[0], professors[1]],
        "exam_dates": [],
    },
    "Distributed Systems": {
        "course": CourseCreate(name="Distributed Systems"),
        "professors": [professors[0], professors[2]],
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
    details["exam_dates"] = generate_exam_dates()


users = professors + [
    AuthUserCreate.model_validate(
        test_student,
        update={"hashed_password": get_password_hash("testpassword")},
    )
]


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
    course_cycle = cycle(courses.items())

    current_student = crud.student.create(obj_in=test_student, session=session)

    for group in groups:
        current_course_name, details = next(course_cycle)
        group = crud.group.create(
            obj_in=group,
            update={
                "creator_id": current_student.id,
                "name": f"{group.name} {current_student.number}",
                "course_name": details["course"].name,
                "exam_date": details["exam_dates"][0],
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
