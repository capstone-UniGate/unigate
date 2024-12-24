import secrets
import string
from unittest.mock import MagicMock
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unigate.core.database import engine
from unigate.main import app
from unigate.models import Student

client: TestClient = TestClient(app)

test_student_password = "testpassword"

def authenticate_user(username = "S1234567") -> dict:
    """
    Logs in the user with the given username and returns the token data.
    """
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
    """
    Creates a private group (or any type you want) and returns the created group data.
    """
    token_data = authenticate_user()
    token = token_data["access_token"]

    group_payload = {
        "id": str(uuid.uuid4()),
        "name": f"TestGroup-{uuid.uuid4().hex[:6]}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Private",
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/groups", json=group_payload, headers=headers)

    assert response.status_code == 200, f"Failed to create group: {response.json()}"
    return response.json()


def test_join_private_group_success() -> None:
    """
    1) Create a private group.
    2) Log in as user 'S4989646'.
    3) Request to join the group.
    4) Ensure that a join request is created (PENDING).
    5) (Optional) Approve that request and verify it's approved.
    """

    # 1) Create the private group
    group_response = create_group()
    created_group_id = group_response["id"]

    # 2) Log in as user 'S4989646'
    token_data = authenticate_user("S4989646")
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    me_response = client.get("/students/me", headers=headers)
    assert me_response.status_code == 200, f"Could not fetch 'me': {me_response.json()}"
    joiner_id = me_response.json()["id"]

    # 3) Ask to join the newly created private group
    join_response = client.post(
        f"/groups/{created_group_id}/join",
        headers=headers,
    )
    # For a private group, your API might return 200 or 400 depending on how you handle "request created" vs. "already requested".
    # Adjust as needed based on your endpoint's actual response:
    assert join_response.status_code in [200, 400], f"Join request failed: {join_response.json()}"

    token_data = authenticate_user()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    # 4) Verify that the join request is present (and is PENDING)
    #    - Typically, you might fetch the user's ID by calling GET /students/me
    me_response = client.get("/students/me", headers=headers)
    assert me_response.status_code == 200, f"Could not fetch 'me': {me_response.json()}"
    me_data = me_response.json()
    user_id = me_data["id"]

    #    - Now, retrieve the pending requests for this group
    requests_response = client.get(f"/groups/{created_group_id}/requests", headers=headers)
    assert requests_response.status_code == 200, f"Could not retrieve requests: {requests_response.json()}"
    requests_data = requests_response.json()

    join_request = next((req for req in requests_data if req["student_id"] == joiner_id), None)
    assert (
        join_request is not None
    ), f"Join request not found for user {joiner_id}. Requests data: {requests_data}"
    assert join_request["status"] == "PENDING"

    # 5) (Optional) Approve the request and verify it's approved
    approve_path = f"groups/{created_group_id}/requests/{join_request['id']}/approve"
    approve_response = client.post(approve_path, headers=headers)
    assert approve_response.status_code == 200, f"Failed to approve request: {approve_response.json()}"

    # Confirm it's now approved
    requests_response = client.get(f"/groups/{created_group_id}/requests", headers=headers)
    assert requests_response.status_code == 200
    requests_data = requests_response.json()
    updated_request = next((req for req in requests_data if req["id"] == join_request["id"]), None)
    assert updated_request["status"] == "APPROVED"