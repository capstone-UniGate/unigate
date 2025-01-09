import uuid

from fastapi.testclient import TestClient
from unigate.main import app

client = TestClient(app)

test_student_password = "testpassword"


def authenticate_user(username="S1234567") -> dict:
    login_payload = {
        "username": username,
        "password": test_student_password,
    }

    response = client.post("/auth/login", data=login_payload)

    assert (
        response.status_code == 200
    ), f"Failed to authenticate user: {response.json()}"
    return response.json()


def create_group() -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]

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


def add_student_to_group(group_id: str):
    token_data = authenticate_user("S4989646")
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = client.post(f"/groups/{group_id}/join", headers=headers)

    assert response.status_code == 200, f"Failed to add student: {response.json()}"

    return client.get("/students/me", headers=headers).json()["id"]


def test_block_user_success():
    group_response = create_group()
    created_group_id = group_response["id"]

    # Ensure the student is added to the group
    added_student_id = add_student_to_group(created_group_id)

    token_data = authenticate_user()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = client.post(
        f"/groups/{created_group_id}/students/{added_student_id}/block",
        headers=headers,
    )

    assert response.status_code == 200, f"Block failed: {response.json()}"
    assert response.json()["id"] == created_group_id

    blocked_student_ids = [
        student["id"] for student in response.json().get("blocked_students", [])
    ]
    assert (
        added_student_id in blocked_student_ids
    ), f"Student {added_student_id} was not blocked."


def test_block_user_group_not_found():
    token_data = authenticate_user()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = client.post(
        f"/groups/{uuid.uuid4()}/students/{uuid.uuid4()}/block",
        headers=headers,
    )

    assert response.status_code == 404, f"Expected 404, got: {response.status_code}"
    assert response.json() == {"detail": "Group not found."}


def test_block_user_student_not_found():
    group_response = create_group()
    created_group_id = group_response["id"]

    token_data = authenticate_user()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = client.post(
        f"/groups/{created_group_id}/students/{uuid.uuid4()}/block",
        headers=headers,
    )

    assert response.status_code == 404, f"Expected 404, got: {response.status_code}"
    assert response.json() == {"detail": "Student not found."}
