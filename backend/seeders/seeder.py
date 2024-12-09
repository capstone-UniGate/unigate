import datetime
import secrets
import uuid

import pytz
from faker import Faker
from loguru import logger
from sqlalchemy import text, create_engine
from sqlmodel import Session
from unigate.core.database import engine
from unigate.models import (
    Group,
    GroupType,
    Join,
    Request,
    RequestStatus,
    Student,
    SuperStudent,
)


def set_default_members_count():
    """
    Ensure the 'members_count' column has a default value of 0 in the database schema.
    """
    db_engine = create_engine(engine.url)
    with db_engine.connect() as connection:
        connection.execute(
            text("ALTER TABLE groups ALTER COLUMN members_count SET DEFAULT 0;")
        )
        logger.info("Default value for 'members_count' set to 0.")


# Helper function to create some dummy data
def create_dummy_data() -> None:
    set_default_members_count()  # Set the default value before creating dummy data
    for _ in range(5):
        create_group_and_members()


def generate_group_name() -> str:
    subjects = [
        "Math",
        "Science",
        "History",
        "Literature",
        "Biology",
        "Physics",
        "Chemistry",
        "Art",
        "Philosophy",
        "Computer Science",
    ]
    adjectives = [
        "Brilliant",
        "Curious",
        "Eager",
        "Energetic",
        "Intelligent",
        "Focused",
        "Ambitious",
        "Dynamic",
        "Inquisitive",
        "Resourceful",
    ]
    mascots = [
        "Scholars",
        "Thinkers",
        "Minds",
        "Learners",
        "Innovators",
        "Explorers",
        "Creators",
        "Wizards",
        "Strategists",
        "Analysts",
    ]

    subject = secrets.choice(subjects)
    adjective = secrets.choice(adjectives)
    mascot = secrets.choice(mascots)

    return f"{adjective} {subject} {mascot}"


def generate_group_category() -> str:
    categories = [
        "Math",
        "Science",
        "History",
        "Literature",
        "Biology",
        "Physics",
        "Chemistry",
        "Art",
        "Philosophy",
        "Computer Science",
    ]
    return secrets.choice(categories)


def create_group_and_members() -> None:
    fake = Faker()
    with Session(engine) as session:
        student = Student(
            id=uuid.uuid4(),
            # hashed_password=fake.password(),
            number=fake.random_int(1000, 100000),
            email=fake.email(),
            name=fake.name(),
            surname=fake.last_name(),
        )

        session.add(student)
        session.commit()

        # Seed groups
        group = Group(
            id=uuid.uuid4(),
            name=generate_group_name(),
            description=fake.sentence(20),
            category=generate_group_category(),
            type=secrets.choice(list(GroupType)),
            creator_id=student.id,
            members_count=0,  # Explicitly set members_count to 0
        )

        session.add(group)
        session.commit()

        # Add the student to super student
        super_student = SuperStudent(
            student_id=student.id,
            group_id=group.id,
        )

        session.add(super_student)
        session.commit()

        # In case the group is public add 10 students to the group
        if group.type == GroupType.PUBLIC:
            for _ in range(10):
                student = Student(
                    id=uuid.uuid4(),
                    hashed_password=fake.password(),
                    number=fake.random_int(1000, 100000),
                    email=fake.email(),
                    name=fake.name(),
                    surname=fake.last_name(),
                )

                session.add(student)
                session.commit()

                join = Join(
                    student_id=student.id,
                    group_id=group.id,
                    date=datetime.datetime.now(tz=pytz.timezone("Europe/Rome")).date(),
                )

                # Increase the member count
                group.members_count += 1

                session.add(join)
                session.commit()

        logger.debug(group.type)

        if group.type == GroupType.PRIVATE:
            for _ in range(10):
                student = Student(
                    id=uuid.uuid4(),
                    hashed_password=fake.password(),
                    number=fake.random_int(1000, 100000),
                    email=fake.email(),
                    name=fake.name(),
                    surname=fake.last_name(),
                )
                session.add(student)
                session.commit()

                # create the request for the students
                request = Request(
                    id=uuid.uuid4(),
                    status=secrets.choice(list(RequestStatus)),
                    student_id=student.id,
                    group_id=group.id,
                )

                session.add(request)
                session.commit()

                if request.status == RequestStatus.APPROVED:
                    join = Join(
                        student_id=student.id,
                        group_id=group.id,
                    )

                    # Increase the member count
                    group.members_count += 1

                    session.add(join)
                    session.commit()


if __name__ == "__main__":
    # Seed the data
    create_dummy_data()