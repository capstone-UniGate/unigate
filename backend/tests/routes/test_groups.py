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

client: TestClient = TestClient(app)

client = TestClient(app)

@pytest.fixture
def mock_session() -> MagicMock:
    session: MagicMock = MagicMock(spec=Session)
    return session


@pytest.fixture
def valid_group_payload() -> dict[str, str]:
    return {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": "12345678-1234-5678-1234-567812345678",
    }


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


def test_create_group_success(valid_group_payload: dict[str, str]) -> None:
    create_student("12345678-1234-5678-1234-567812345678")

    response = client.post("/groups/create", json=valid_group_payload)
    assert response.status_code == 201
    data: dict[str, str] = response.json()
    assert data["name"] == valid_group_payload["name"]
    assert data["description"] == valid_group_payload["description"]
    assert data["category"] == valid_group_payload["category"]
    assert data["type"] == valid_group_payload["type"]
    assert data["creator_id"] == valid_group_payload["creator_id"]


def test_create_group_duplicate_name(valid_group_payload: dict[str, str]) -> None:
    # Randomize the group name for the initial creation
    randomized_group_name = (
        f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}"
    )
    valid_group_payload["name"] = randomized_group_name

    # Call the success test manually to ensure the group is created
    create_student("12345678-1234-5678-1234-567812345678")  # Ensure the creator exists
    response = client.post("/groups/create", json=valid_group_payload)
    assert response.status_code == 201  # Ensure the group was created successfully

    # Attempt to create the group again with the same randomized name
    duplicate_response = client.post("/groups/create", json=valid_group_payload)
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Group with this name already exists."


def test_create_group_invalid_type(valid_group_payload: dict[str, str]) -> None:
    invalid_payload: dict[str, str] = valid_group_payload.copy()
    invalid_payload["type"] = "InvalidType"
    invalid_payload["name"] = "NewName1"
    response = client.post("/groups/create", json=invalid_payload)
    assert response.status_code == 400
    assert "Invalid group type" in response.json()["detail"]


def test_create_group_non_existing_creator_id(
    mock_session: MagicMock, valid_group_payload: dict[str, str]
) -> None:
    # Ensure the creator_id remains a valid UUID string
    valid_group_payload["creator_id"] = str(
        UUID("12345678-1234-5678-1234-567812345679")
    )
    valid_group_payload["name"] = "NewName3"
    # Simulate a non-existing creator_id
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    response = client.post("/groups/create", json=valid_group_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Creator ID does not exist in students table."