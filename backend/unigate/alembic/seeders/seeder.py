import datetime
import random
import uuid

import pytz
from faker import Faker
from loguru import logger
from sqlmodel import Session
from unigate.core.database import engine
from unigate.models import (
    Group,
    GroupType,
    Join,
    Request,
    Student,
    SuperStudent,
)


# Helper function to create some dummy data
def create_dummy_data() -> None:
    for _ in range(5):
        create_group_and_members()


def generate_group_name():
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

    subject = random.choice(subjects)
    adjective = random.choice(adjectives)
    mascot = random.choice(mascots)

    return f"{adjective} {subject} {mascot}"


def generate_group_category():
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
    return random.choice(categories)


def create_group_and_members():
    fake = Faker()
    with Session(engine) as session:
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

        # Seed groups
        group = Group(
            id=fake.uuid4(),
            name=generate_group_name(),
            description=fake.sentence(20),
            category=generate_group_category(),
            type=random.choice(["PUBLIC", "PRIVATE"]),
            creator_id=student.id,
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
        # Create 10 more students and assign them to the group as members
        if group.type == GroupType.PUBLIC:
            for i in range(10):
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
                group.members_count = group.members_count + 1

                session.add(join)
                session.commit()

        logger.debug(group.type)

        if group.type == GroupType.PRIVATE:
            for i in range(10):
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
                    status=random.choice(["PENDING", "APPROVED", "REJECTED"]),
                    student_id=student.id,
                    group_id=group.id,
                )

                session.add(request)
                session.commit()

                if request.status == "APPROVED":
                    join = Join(
                        student_id=student.id,
                        group_id=group.id,
                    )

                    # Increase the member count
                    group.members_count = group.members_count + 1

                    session.add(join)
                    session.commit()


if __name__ == "__main__":
    # Seed the data
    create_dummy_data()
