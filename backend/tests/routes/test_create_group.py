import secrets
import string
import uuid
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unigate.core.database import engine
from unigate.main import app
from unigate.models import Student

client: TestClient = TestClient(app)

# Test user credentials
test_student_username = "S1234567"
test_student_password = "testpassword"
test_student_id = str(uuid.uuid4())


def authenticate_user() -> dict:
    """Authenticate a test user and return the access token."""
    login_payload = {
        "username": test_student_username,
        "password": test_student_password,
    }

    response = client.post("/auth/login", data=login_payload)
    assert (
        response.status_code == 200
    ), f"Failed to authenticate user: {response.json()}"
    return response.json()


def create_student(student_id: str) -> None:
    """Create a test student if not already present in the database."""
    with Session(engine) as session:
        # Check if the student already exists
        existing_student = session.query(Student).filter_by(id=UUID(student_id)).first()
        if existing_student:
            return

        # Generate unique email and number
        unique_number = secrets.randbelow(1_000_000)
        unique_email = f"teststudent{unique_number}@example.com"

        student = Student(
            id=UUID(student_id),
            hashed_password="hashedpassword123",
            number=unique_number,
            email=unique_email,
            name="Test",
            surname="Student",
        )
        session.add(student)
        session.commit()


def test_create_group_success() -> None:
    """Test group creation with valid data."""
    create_student(test_student_id)
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    valid_group_payload = {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": test_student_id,
    }

    response = client.post("/groups", json=valid_group_payload, headers=headers)
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert data["name"] == valid_group_payload["name"]
    assert data["description"] == valid_group_payload["description"]
    assert data["category"] == valid_group_payload["category"]
    assert data["type"] == valid_group_payload["type"]
    assert "students" in data
    assert "super_students" in data
    assert "blocked_students" in data


def test_create_group_invalid_type() -> None:
    """Test group creation with invalid group type."""
    create_student(test_student_id)
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    invalid_group_payload = {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "InvalidType",
        "creator_id": test_student_id,
    }

    response = client.post("/groups", json=invalid_group_payload, headers=headers)
    assert response.status_code == 422


def test_get_group_info() -> None:
    """Test retrieval of group information."""
    create_student(test_student_id)
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    valid_group_payload = {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": test_student_id,
    }
    create_group_response = client.post(
        "/groups", json=valid_group_payload, headers=headers
    )
    assert create_group_response.status_code == 200, "Group creation failed"
    created_group = create_group_response.json()

    # Retrieve the group by its ID
    group_id = created_group.get("id")
    assert group_id, "Group ID not found in response"

    response = client.get(f"/groups/{group_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == created_group
