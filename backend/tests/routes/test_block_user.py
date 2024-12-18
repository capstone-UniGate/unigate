import secrets
import string
from uuid import UUID
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Literal

from unigate.main import app
from unigate.models import Student
from unigate.core.database import engine

client = TestClient(app)

# Constants
ADMIN_USERNAME = "S4989646"  # Admin (Super Student) username
NON_ADMIN_USERNAME = "S1234567"  # Non-admin student username
PASSWORD = "testpassword"
STUDENT_ID = "dd2cb931-3373-4fc1-a689-864102fadd95"

def authenticate_user(user_type: Literal["admin", "non-admin"] = "admin") -> str:
    """
    Authenticate a user and return the access token.
    :param user_type: 'admin' or 'non-admin' to determine the user type.
    :return: Access token string.
    """
    username = ADMIN_USERNAME if user_type == "admin" else NON_ADMIN_USERNAME
    response = client.post(
        "/auth/login", data={"username": username, "password": PASSWORD}
    )
    assert (
        response.status_code == 200
    ), f"Failed to authenticate user: {response.json()}"
    return response.json()["access_token"]

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
            number=12345,  # Unique student number
            email="teststudent@example.com",  # Unique email
            name="Test",
            surname="Student",
        )
        session.add(student)
        session.commit()

def test_get_group_info() -> str:
    """
    Test retrieving a group by its ID.
    :return: The ID of the created group.
    """
    # Create the student and authenticate
    create_student(STUDENT_ID)
    token = authenticate_user()
    headers = {"Authorization": f"Bearer {token}"}

    # Create a group first
    valid_group_payload = {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": STUDENT_ID,
    }
    create_group_response = client.post("/groups", json=valid_group_payload, headers=headers)
    created_group = create_group_response.json()

    # Now retrieve the group by its ID
    group_id = created_group["id"]
    response = client.get(f"/groups/{group_id}", headers=headers)

    # Assertions to verify the group details
    assert response.status_code == 200
    assert response.json() == created_group

    return group_id

def test_student_request_join_group() -> str:
    """Test that a student can successfully request to join a group."""
    # Retrieve a group ID
    group_id = test_get_group_info()

    # Authenticate as non-admin student
    token = authenticate_user(user_type="non-admin")
    headers = {"Authorization": f"Bearer {token}"}

    # Request to join group
    response = client.post(f"/groups/{group_id}/join", headers=headers)

    # Assertions
    assert response.status_code == 200, f"Join request failed: {response.json()}"
    data = response.json()
    assert data["id"] == group_id, "Group ID does not match."
    assert "name" in data, "Group 'name' is missing in the response."
    assert "students" in data, "Group 'students' list is missing."

    return group_id

def test_block_user() -> None:
    """Test that the group admin can successfully block a user."""
    # Retrieve a group ID and ensure a student requests to join
    group_id = test_student_request_join_group()

    # Authenticate as group admin
    admin_token = authenticate_user(user_type="admin")
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Block the student
    response = client.post(
        f"/groups/{group_id}/students/{STUDENT_ID}/block", headers=headers
    )

    # Assertions
    assert response.status_code == 200, f"Blocking user failed: {response.json()}"
    data = response.json()
    assert data["id"] == group_id, "Group ID does not match."

    # Verify the student is in the 'blocked_students' list
    blocked_students = data.get("blocked_students", [])
    assert any(
        student["id"] == STUDENT_ID for student in blocked_students
    ), "Student was not successfully blocked."

def test_unblock_user() -> None:
    """Test that the group admin can successfully unblock a user."""
    # Retrieve a group ID and ensure a student is blocked
    group_id = test_student_request_join_group()

    # Authenticate as group admin
    admin_token = authenticate_user(user_type="admin")
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Block the student first
    client.post(f"/groups/{group_id}/students/{STUDENT_ID}/block", headers=headers)

    # Unblock the student
    response = client.post(
        f"/groups/{group_id}/students/{STUDENT_ID}/unblock", headers=headers
    )

    # Assertions
    assert response.status_code == 200, f"Unblocking user failed: {response.json()}"
    data = response.json()
    assert data["id"] == group_id, "Group ID does not match."

    # Verify the student is not in the 'blocked_students' list
    blocked_students = data.get("blocked_students", [])
    assert not any(
        student["id"] == STUDENT_ID for student in blocked_students
    ), "Student was not successfully unblocked."

def test_non_admin_cannot_block_user() -> None:
    """Test that a non-admin user cannot block another user."""
    # Retrieve a group ID and ensure a student requests to join
    group_id = test_student_request_join_group()

    # Authenticate as a non-admin user
    non_admin_token = authenticate_user(user_type="non-admin")
    headers = {"Authorization": f"Bearer {non_admin_token}"}

    # Attempt to block a user
    response = client.post(
        f"/groups/{group_id}/students/{STUDENT_ID}/block", headers=headers
    )

    # Assertions
    assert response.status_code == 403, "Expected 403 Forbidden for non-admin user."
    assert response.json()["detail"] == "You are not a super student of this group"

def test_non_admin_cannot_unblock_user() -> None:
    """Test that a non-admin user cannot unblock another user."""
    # Retrieve a group ID and ensure a student is blocked
    group_id = test_student_request_join_group()

    # Authenticate as group admin and block the student
    admin_token = authenticate_user(user_type="admin")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    client.post(f"/groups/{group_id}/students/{STUDENT_ID}/block", headers=admin_headers)

    # Authenticate as a non-admin user
    non_admin_token = authenticate_user(user_type="non-admin")
    headers = {"Authorization": f"Bearer {non_admin_token}"}

    # Attempt to unblock a user
    response = client.post(
        f"/groups/{group_id}/students/{STUDENT_ID}/unblock", headers=headers
    )

    # Assertions
    assert response.status_code == 403, "Expected 403 Forbidden for non-admin user."
    assert response.json()["detail"] == "You are not a super student of this group"
