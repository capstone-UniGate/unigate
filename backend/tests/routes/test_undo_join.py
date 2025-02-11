import uuid

from fastapi.testclient import TestClient
from unigate.main import app

client = TestClient(app)

test_student_username = "S1234567"
test_student_password = "testpassword"
group_id = str(uuid.uuid4())


def authenticate_user(
    username=test_student_username, password=test_student_password
) -> dict:
    login_payload = {
        "username": username,
        "password": password,
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == 200, (
        f"Failed to authenticate user: {response.json()}"
    )
    return response.json()


def create_private_group() -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    course = client.get("/courses").json()[0]
    group_payload = {
        "id": group_id,
        "name": f"TestGroup-{uuid.uuid4().hex[:6]}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Private",
        "course_name": course["name"],
        "exam_date": course["exams"][0]["date"],
    }

    response = client.post("/groups", json=group_payload, headers=headers)
    assert response.status_code == 200, f"Failed to create group: {response.json()}"
    return response.json()


def test_undo_join_request_success():
    group_response = create_private_group()
    created_group_id = group_response["id"]

    other_user_token_data = authenticate_user(username="S4989646")
    other_user_token = other_user_token_data["access_token"]
    other_user_number = "4989646"
    other_user_headers = {"Authorization": f"Bearer {other_user_token}"}

    join_response = client.post(
        f"/groups/{created_group_id}/join", headers=other_user_headers
    )
    assert join_response.status_code == 200, (
        f"Join request failed: {join_response.json()}"
    )

    owner_token_data = authenticate_user(username="S1234567")
    owner_token = owner_token_data["access_token"]
    owner_headers = {"Authorization": f"Bearer {owner_token}"}

    requests_response = client.get(
        f"/groups/{created_group_id}/requests", headers=owner_headers
    )
    assert requests_response.status_code == 200, (
        f"Failed to fetch requests: {requests_response.json()}"
    )

    requests_data = requests_response.json()
    assert len(requests_data) > 0, "No join requests found."

    join_request = next(
        (
            req
            for req in requests_data
            if str(req["student"]["number"]) == other_user_number
        ),
        None,
    )
    assert join_request is not None, (
        f"Join request not found. Debug data: {requests_data}"
    )

    undo_response = client.delete(
        f"/groups/{created_group_id}/requests/undo", headers=other_user_headers
    )
    assert undo_response.status_code == 200, (
        f"Failed to undo join request: {undo_response.json()}"
    )

    updated_requests_response = client.get(
        f"/groups/{created_group_id}/requests", headers=owner_headers
    )
    assert updated_requests_response.status_code == 200, (
        f"Failed to fetch requests: {updated_requests_response.json()}"
    )

    updated_requests_data = updated_requests_response.json()
    assert not any(
        req["student"]["number"] == other_user_number for req in updated_requests_data
    ), f"Join request was not undone: {updated_requests_data}"
