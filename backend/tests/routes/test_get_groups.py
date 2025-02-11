from uuid import uuid4

from fastapi.testclient import TestClient
from unigate.main import app

client: TestClient = TestClient(app)

# Test user credentials
test_student_username = "S1234567"
test_student_password = "testpassword"
test_student_id = "d6dcf3b1-425a-4864-88d3-525decebef18"


def authenticate_user() -> dict:
    login_payload = {
        "username": test_student_username,
        "password": test_student_password,
    }

    response = client.post("/auth/login", data=login_payload)

    assert response.status_code == 200, (
        f"Failed to authenticate user: {response.json()}"
    )
    return response.json()


def create_group(student_id: str) -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]

    course = client.get("/courses").json()[0]
    group_payload = {
        "id": str(uuid4()),  # Generate a new UUID for the group
        "name": f"TestGroup-{uuid4().hex[:6]}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": student_id,
        "course_name": course["name"],
        "exam_date": course["exams"][0]["date"],
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/groups", json=group_payload, headers=headers)

    assert response.status_code == 200, f"Failed to create group: {response.json()}"
    return response.json()


def test_get_groups_list() -> None:
    create_group(student_id=test_student_id)

    token_data = authenticate_user()
    token = token_data["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/groups", headers=headers)

    assert response.status_code == 200, (
        f"Failed to retrieve groups list: {response.json()}"
    )
    assert isinstance(response.json(), list), "Response should be a list of groups"
    assert len(response.json()) > 0, "There should be at least one group"
