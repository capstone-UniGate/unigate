import datetime
import uuid

import pytz
from loguru import logger
from sqlmodel import Session
from unigate.core.database import (
    engine,  # Assuming you have a central engine for the database
)

# Import your existing models from the project
from unigate.models import (  # Adjust import path
    Group,
    Join,
    Request,
    Student,
    SuperStudent,
)


# Helper function to create some dummy data
def create_dummy_data() -> None:
    with Session(engine) as session:
        # Seed students
        student1 = Student(
            id=uuid.uuid4(),
            hashed_password="hashedpassword1",  # noqa: S106
            number=101,
            email="student1@example.com",
            name="Alice",
            surname="Smith",
        )
        student2 = Student(
            id=uuid.uuid4(),
            hashed_password="hashedpassword2",  # noqa: S106
            number=102,
            email="student2@example.com",
            name="Bob",
            surname="Johnson",
        )
        session.add_all([student1, student2])
        session.commit()

        # Seed groups
        group1 = Group(
            id=uuid.uuid4(),
            name="Math Club",
            description="A club for math enthusiasts",
            category="Education",
            type="PUBLIC",
            creator_id=student1.id,
        )
        group2 = Group(
            id=uuid.uuid4(),
            name="Science Society",
            description="Exploring the wonders of science",
            category="Science",
            type="PRIVATE",
            creator_id=student2.id,
        )
        session.add_all([group1, group2])
        session.commit()

        # Seed joins
        join1 = Join(
            student_id=student1.id,
            group_id=group1.id,
            date=datetime.datetime.now(tz=pytz.timezone("Europe/Rome")).date(),
        )
        join2 = Join(
            student_id=student2.id,
            group_id=group2.id,
            date=datetime.datetime.now(tz=pytz.timezone("Europe/Rome")).date(),
        )
        session.add_all([join1, join2])
        session.commit()

        # Seed requests
        request1 = Request(
            id=uuid.uuid4(),
            status="PENDING",
            student_id=student1.id,
            group_id=group2.id,
        )
        request2 = Request(
            id=uuid.uuid4(),
            status="APPROVED",
            student_id=student2.id,
            group_id=group1.id,
        )
        session.add_all([request1, request2])
        session.commit()

        # Seed super_students
        super_student1 = SuperStudent(student_id=student1.id, group_id=group1.id)
        super_student2 = SuperStudent(student_id=student2.id, group_id=group2.id)
        session.add_all([super_student1, super_student2])
        session.commit()

        logger.debug("Dummy data seeded successfully!")


if __name__ == "__main__":
    # Seed the data
    create_dummy_data()