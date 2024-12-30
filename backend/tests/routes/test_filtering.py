import uuid

import pytest
from fastapi.testclient import TestClient
from unigate.main import app

client = TestClient(app)

test_student_username = "S1234567"
test_student_password = "testpassword"


def authenticate_user(
    username=test_student_username, password=test_student_password
) -> dict:
    login_payload = {
        "username": username,
        "password": password,
    }
    response = client.post("/auth/login", data=login_payload)
    assert (
        response.status_code == 200
    ), f"Failed to authenticate user: {response.json()}"
    return response.json()


def create_group() -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    group_payload = {
        "id": uuid.uuid4(),
        "name": f"TestGroup-{uuid.uuid4().hex[:6]}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "course_name": "Test Course",
        "exam_date": "2025-01-01",
        "date": "2024-01-01",
    }

    response = client.post("/groups", json=group_payload, headers=headers)
    assert response.status_code == 200, f"Failed to create group: {response.json()}"
    return response.json()


@pytest.mark.parametrize(
    "params",
    [
        ({"course": "Test Course"}),
        ({"course": "Test Course", "is_public": True}),
        ({"course": "Test Course", "is_public": False}),
        ({"course": "Test Course", "exam_date": "2024-01-15"}),
        ({"course": "Test Course", "order": "Newest"}),
        ({"course": "Test Course", "participants": 2}),
    ],
)
def test_search(params):
    response = client.get("groups/search", params=params)
    assert response.status_code == 200


def test_invalid_date():
    response = client.get(
        "groups/search", params={"course": "Test Course", "exam_date": "invalid-date"}
    )
    assert response.status_code == 422


def test_missing_course():
    response = client.get("groups/search", params={})
    assert response.status_code == 422


@pytest.mark.parametrize(
    "params,expected_status",
    [
        ({"is_public": True}, 422),
        ({"exam_date": "2025-01-15"}, 422),
        ({"order": "Newest"}, 422),
    ],
)
def test_missing_course_with_other_params(params, expected_status):
    response = client.get("groups/search", params=params)
    assert response.status_code == expected_status


def test_empty_course_param():
    response = client.get("groups/search", params={"course": ""})
    assert response.status_code == 200
