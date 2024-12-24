import uuid

from fastapi.testclient import TestClient
from unigate.main import app

client = TestClient(app)

test_student_username = "S1234567"
test_student_password = "testpassword"
group_id = str(uuid.uuid4())


def authenticate_user(username=test_student_username, password=test_student_password) -> dict:
    """
    Authenticate a user and return their token data.
    """
    login_payload = {
        "username": username,
        "password": password,
    }
    response = client.post("/auth/login", data=login_payload)
    assert (
        response.status_code == 200
    ), f"Failed to authenticate user: {response.json()}"
    return response.json()


def create_private_group() -> dict:
    """
    Create a private group and return its details.
    """
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    group_payload = {
        "id": group_id,
        "name": f"TestGroup-{uuid.uuid4().hex[:6]}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Private",
    }

    response = client.post("/groups", json=group_payload, headers=headers)
    assert response.status_code == 200, f"Failed to create group: {response.json()}"
    return response.json()


def test_undo_join_request_success():
    """
    Test that a user can successfully undo their join request to a private group.
    """

    # Create a private group
    group_response = create_private_group()
    created_group_id = group_response["id"]

    # Authenticate another user to send a join request
    other_user_token_data = authenticate_user(username="4989646")
    other_user_token = other_user_token_data["access_token"]
    other_user_headers = {"Authorization": f"Bearer {other_user_token}"}

    # Send a join request
    join_response = client.post(f"/groups/{created_group_id}/join", headers=other_user_headers)
    assert join_response.status_code == 200, f"Join request failed: {join_response.json()}"

    # Re-authenticate as the group owner (S1234567) to check the requests
    owner_token_data = authenticate_user(username="1234567")
    owner_token = owner_token_data["access_token"]
    owner_headers = {"Authorization": f"Bearer {owner_token}"}

    # Check that the join request exists
    requests_response = client.get(f"/groups/{created_group_id}/requests", headers=owner_headers)
    assert requests_response.status_code == 200, f"Failed to fetch requests: {requests_response.json()}"
    requests_data = requests_response.json()
    assert len(requests_data) > 0, "No join requests found."

    # Verify that the join request is from the correct user
    join_request = next(
        (req for req in requests_data if req["student_id"] == other_user_token_data["user_id"]), None
    )
    assert join_request is not None, "Join request not found."

    # Undo the join request as the requesting user
    undo_response = client.delete(f"/groups/{created_group_id}/requests/undo", headers=other_user_headers)
    assert undo_response.status_code == 204, f"Failed to undo join request: {undo_response.json()}"

    # Re-authenticate as the group owner again to check if the request is gone
    updated_requests_response = client.get(f"/groups/{created_group_id}/requests", headers=owner_headers)
    assert updated_requests_response.status_code == 200, f"Failed to fetch requests: {updated_requests_response.json()}"
    updated_requests_data = updated_requests_response.json()
    assert not any(req["student_id"] == other_user_token_data["user_id"] for req in updated_requests_data), (
        f"Join request was not undone: {updated_requests_data}"
    )
