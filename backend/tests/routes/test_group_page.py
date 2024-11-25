import secrets
import string
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unigate.core.database import engine
from unigate.main import app
from unigate.models import Group, Student

client: TestClient = TestClient(app)


@pytest.fixture
def mock_session() -> MagicMock:
    session: MagicMock = MagicMock(spec=Session)
    return session


def create_student(student_id: str) -> None:
    """
    Check if a Student record exists, and create one if it does not.

    Args:
        student_id (str): The UUID of the student to check or insert.
    """
    with Session(engine) as session:
        # Check if the student already exists
        existing_student = session.query(Student).filter_by(id=UUID(student_id)).first()
        if existing_student:
            return

        # Create a new student record
        student = Student(
            id=UUID(student_id),
            hashed_password="hashedpassword123",  # noqa: S106  # Replace with actual hashed password logic
            number=12345,  # Unique student number
            email="teststudent@example.com",  # Unique email
            name="Test",
            surname="Student",
        )
        session.add(student)
        session.commit()


def create_group(student_id: str, group_id: str) -> dict[str, str]:
    group_payload = {
        "id": group_id,
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": student_id,
    }

    with Session(engine) as session:
        existing_group = session.query(Group).filter_by(id=UUID(group_id)).first()
        if existing_group is not None:
            return {
                "id": str(existing_group.id),
                "name": existing_group.name,
                "description": existing_group.description,
                "category": existing_group.category,
                "type": str(existing_group.type.value),
                "creator_id": str(student_id),
            }

    response = client.post("/groups/create", json=group_payload)
    return response.json()


def test_get_group_info() -> None:
    student_id = "12345678-1234-5678-1234-567812345678"
    create_student(student_id=student_id)
    group_id = "11111111-1111-1111-1111-111111111111"
    group = create_group(student_id=student_id, group_id=group_id)
    response = client.get("/groups/" + str(group_id))
    assert response.status_code == 200
    assert response.json() == group


def test_group_not_found() -> None:
    group_id = "11111111-1111-1111-2111-111111111111"
    response = client.get("/groups/" + str(group_id))
    assert response.status_code == 404
    assert response.json() == {"detail": "Group not found."}
