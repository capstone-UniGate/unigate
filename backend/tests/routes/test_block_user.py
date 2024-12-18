from typing import Literal

from fastapi.testclient import TestClient
from unigate.main import app

client = TestClient(app)

# Constants
ADMIN_USERNAME = "S4989646"  # Admin (Super Student) username
NON_ADMIN_USERNAME = "S1234567"  # Non-admin student username
PASSWORD = ""  # Password for test users: testpassword
GROUP_ID = "960b1adf-6f4e-4179-ba78-df55a3f1e59b"
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


def test_student_request_join_group() -> None:
    """Test that a student can successfully request to join a group."""
    # Authenticate as non-admin student
    token = authenticate_user(user_type="non-admin")
    headers = {"Authorization": f"Bearer {token}"}

    # Request to join group
    response = client.post(f"/groups/{GROUP_ID}/join", headers=headers)

    # Assertions
    assert response.status_code == 200, f"Join request failed: {response.json()}"
    data = response.json()
    assert data["id"] == GROUP_ID, "Group ID does not match."
    assert "name" in data, "Group 'name' is missing in the response."
    assert "students" in data, "Group 'students' list is missing."


def test_block_user() -> None:
    """Test that the group admin can successfully block a user."""
    # Authenticate as group admin
    admin_token = authenticate_user(user_type="admin")
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Block the student
    response = client.post(
        f"/groups/{GROUP_ID}/students/{STUDENT_ID}/block", headers=headers
    )

    # Assertions
    assert response.status_code == 200, f"Blocking user failed: {response.json()}"
    data = response.json()
    assert data["id"] == GROUP_ID, "Group ID does not match."

    # Verify the student is in the 'blocked_students' list
    blocked_students = data.get("blocked_students", [])
    assert any(
        student["id"] == STUDENT_ID for student in blocked_students
    ), "Student was not successfully blocked."


def test_unblock_user() -> None:
    """Test that the group admin can successfully unblock a user."""
    # Authenticate as group admin
    admin_token = authenticate_user(user_type="admin")
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Unblock the student
    response = client.post(
        f"/groups/{GROUP_ID}/students/{STUDENT_ID}/unblock", headers=headers
    )

    # Assertions
    assert response.status_code == 200, f"Unblocking user failed: {response.json()}"
    data = response.json()
    assert data["id"] == GROUP_ID, "Group ID does not match."

    # Verify the student is not in the 'blocked_students' list
    blocked_students = data.get("blocked_students", [])
    assert not any(
        student["id"] == STUDENT_ID for student in blocked_students
    ), "Student was not successfully unblocked."


def test_non_admin_cannot_block_user() -> None:
    """Test that a non-admin user cannot block another user."""
    # Authenticate as a non-admin user
    non_admin_token = authenticate_user(user_type="non-admin")
    headers = {"Authorization": f"Bearer {non_admin_token}"}

    # Attempt to block a user
    response = client.post(
        f"/groups/{GROUP_ID}/students/{STUDENT_ID}/block", headers=headers
    )

    # Assertions
    assert response.status_code == 403, "Expected 403 Forbidden for non-admin user."
    assert response.json()["detail"] == "You are not a super student of this group"


def test_non_admin_cannot_unblock_user() -> None:
    """Test that a non-admin user cannot unblock another user."""
    # Authenticate as a non-admin user
    non_admin_token = authenticate_user(user_type="non-admin")
    headers = {"Authorization": f"Bearer {non_admin_token}"}

    # Attempt to unblock a user
    response = client.post(
        f"/groups/{GROUP_ID}/students/{STUDENT_ID}/unblock", headers=headers
    )

    # Assertions
    assert response.status_code == 403, "Expected 403 Forbidden for non-admin user."
    assert response.json()["detail"] == "You are not a super student of this group"
