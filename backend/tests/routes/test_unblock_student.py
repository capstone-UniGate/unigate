import uuid

from fastapi.testclient import TestClient
from sqlalchemy.future import select
from unigate.core.database import engine
from unigate.main import app
from unigate.models import Block, Group

client = TestClient(app)


test_student_username = "S1234567"
test_student_password = "testpassword"
test_student_id = "d6dcf3b1-425a-4864-88d3-525decebef18"


def authenticate_user() -> dict:
    login_payload = {
        "username": test_student_username,
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

    group_payload = {
        "id": str(uuid.uuid4()),
        "name": f"TestGroup-{uuid.uuid4().hex[:6]}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/groups", json=group_payload, headers=headers)

    assert response.status_code == 200, f"Failed to create group: {response.json()}"
    return response.json()


def create_blocked_student(student_id: str, group_id: str) -> None:
    with engine.begin() as connection:
        group_result = connection.execute(
            select(Group).where(Group.id == uuid.UUID(group_id))
        ).scalar_one_or_none()

        if not group_result:
            raise ValueError(f"Group {group_id} does not exist.")

        connection.execute(
            Block.__table__.insert().values(
                student_id=uuid.UUID(student_id), group_id=uuid.UUID(group_id)
            )
        )


# Tests
def test_unblock_user_success():
    group_response = create_group()
    created_group_id = group_response["id"]

    create_blocked_student(test_student_id, created_group_id)

    token_data = authenticate_user()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = client.post(
        f"/groups/{created_group_id}/students/{test_student_id}/unblock",
        headers=headers,
    )

    assert response.status_code == 200, f"Unblock failed: {response.json()}"
    assert response.json()["id"] == created_group_id
    assert test_student_id not in response.json().get("blocked_students", [])


def test_unblock_user_group_not_found():
    token_data = authenticate_user()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = client.post(
        f"/groups/{uuid.uuid4()}/students/{uuid.uuid4()}/unblock",
        headers=headers,
    )

    assert response.status_code == 404, f"Expected 404, got: {response.status_code}"
    assert response.json() == {"detail": "Group not found."}


def test_unblock_user_student_not_found():
    group_response = create_group()
    created_group_id = group_response["id"]

    token_data = authenticate_user()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = client.post(
        f"/groups/{created_group_id}/students/{uuid.uuid4()}/unblock",
        headers=headers,
    )

    assert response.status_code == 404, f"Expected 404, got: {response.status_code}"
    assert response.json() == {"detail": "Student not found."}
