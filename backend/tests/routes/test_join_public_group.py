import uuid

from fastapi.testclient import TestClient
from unigate.main import app

client = TestClient(app)

test_student_password = "testpassword"

# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------


def authenticate_user(username="S1234567") -> dict:
    """
    Logs in a user and returns the authentication token.
    """
    login_payload = {
        "username": username,
        "password": test_student_password,
    }

    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == 200, (
        f"Failed to authenticate user: {response.json()}"
    )
    return response.json()


def create_group(token: str) -> dict:
    """
    Creates a public group and returns the group data.
    """

    course = client.get("/courses").json()[0]
    group_payload = {
        "id": str(uuid.uuid4()),
        "name": f"TestGroup-{uuid.uuid4().hex[:6]}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "course_name": course["name"],
        "exam_date": course["exams"][0]["date"],
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/groups", json=group_payload, headers=headers)

    assert response.status_code == 200, f"Failed to create group: {response.json()}"
    return response.json()


# -------------------------------------------------------------------
# Test Cases
# -------------------------------------------------------------------


def test_student_non_existent() -> None:
    """
    If the student doesn't exist in the DB, joining a public group should fail
    with a 403 or 404 response.
    """

    # Log in as the creator and create a group
    creator_data = authenticate_user("S1234567")
    creator_token = creator_data["access_token"]
    group_info = create_group(creator_token)
    created_group_id = group_info["id"]

    # Use a fake token to simulate a non-existent student
    headers = {"Authorization": "Bearer Cerioli Sium"}

    response = client.post(f"/groups/{created_group_id}/join", headers=headers)
    assert response.status_code == 403, (
        f"Unexpected status code: {response.status_code}"
    )
    assert response.json() == {"detail": "Could not validate credentials"}


def test_group_non_existent() -> None:
    """
    If the group doesn't exist in the DB, joining should fail with 404 response.
    """

    # Log in as a valid user
    user_data = authenticate_user("S4989646")
    user_token = user_data["access_token"]

    # Use a random group ID that doesn't exist
    random_group_id = str(uuid.uuid4())

    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post(f"/groups/{random_group_id}/join", headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Group not found."}


def test_valid_join() -> None:
    """
    A valid scenario where a user successfully joins a public group.
    Should return the group object with the updated list of students.
    """

    # Log in as the creator and create a group
    creator_data = authenticate_user("S1234567")
    creator_token = creator_data["access_token"]
    group_info = create_group(creator_token)
    created_group_id = group_info["id"]

    # Log in as another user to join the group
    joiner_data = authenticate_user("S4989646")
    joiner_token = joiner_data["access_token"]

    headers = {"Authorization": f"Bearer {joiner_token}"}
    response = client.post(f"/groups/{created_group_id}/join", headers=headers)

    assert response.status_code == 200
    group_response = response.json()

    joiner_id = client.get("/students/me", headers=headers).json()["id"]

    # Check that the group contains the joiner's details
    assert "students" in group_response, "Expected 'students' field in response"
    students = group_response["students"]
    assert any(student["id"] == joiner_id for student in students), (
        f"Joiner {joiner_id} not found in group students list"
    )
