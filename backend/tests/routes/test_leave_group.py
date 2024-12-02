import secrets
import string
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unigate.core.database import engine
from unigate.main import app
from unigate.models import Student

client = TestClient(app)

student_id = "12745678-1234-5678-1234-567812345678"
group_id = "12375678-1234-5678-1234-567812345677"
student_id2 = "12345678-1234-5778-1234-567812345678"


@pytest.fixture
def mock_session() -> MagicMock:
    session: MagicMock = MagicMock(spec=Session)
    return session


def create_student(student_id: str, number: int, mail: str) -> None:
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
            number=number,  # Unique student number
            email=mail + "@example.com",  # Unique email
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
    response = client.post("/groups/create", json=group_payload)
    return response.json()


def test_group_non_existant() -> None:
    create_student(student_id=student_id, number=12347, mail="testsdstudent")
    r = client.post(
        "/groups/" + group_id + "/leave",
        params={
            "student_id": student_id,
            "group_id": group_id,
        },
    )
    assert r.status_code == 200
    assert r.json() == "The group doesn't exist"


def test_student_non_existent() -> None:
    create_group(student_id=student_id, group_id=group_id)

    r = client.post(
        "/groups/" + group_id + "/leave",
        params={
            "student_id": student_id,
            "group_id": group_id,
        },
    )
    assert r.status_code == 200
    assert r.json() == "The student is not part of the group"


def test_valid_leave() -> None:
    create_student(student_id=student_id2, number=12349, mail="testsstudent")
    group = client.get("/groups/" + group_id)

    client.post(
        "/groups/join_public_group",
        params={
            "student_id": student_id,
            "group_id": group_id,
        },
    )
    client.post(
        "/groups/join_public_group",
        params={
            "student_id": student_id2,
            "group_id": group_id,
        },
    )

    response = client.post(
        "/groups/" + group_id + "/leave",
        params={
            "group_id": group_id,
            "student_id": student_id2,
        },
    )

    assert response.status_code == 200
    assert response.json() == "The student has been removed successfully"

    r = client.get("/groups/" + group_id)

    assert r.status_code == 200
    assert r.json() == group.json()


def test_valid_leave_no_members(client: TestClient) -> None:
    response = client.post(
        "/groups/" + group_id + "/leave",
        params={
            "student_id": student_id,
            "group_id": group_id,
        },
    )

    assert response.status_code == 200
    assert response.json() == "The student has been removed successfully"

    r = client.get("/groups/" + group_id)

    assert r.status_code == 404
    assert r.json() == {"detail": "Group not found."}
