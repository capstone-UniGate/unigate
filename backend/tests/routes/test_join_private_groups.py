import secrets
import string
from unittest.mock import MagicMock
from uuid import UUID
import random

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unigate.core.database import engine
from unigate.main import app
from unigate.models import Student

client: TestClient = TestClient(app)


@pytest.fixture
def mock_session() -> MagicMock:
    session: MagicMock = MagicMock(spec=Session)
    return session


@pytest.fixture
def valid_private_group_payload() -> dict[str, str]:
    return {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Private",
        "creator_id": "12345678-1234-5678-1234-567812345678",
    }


def create_student(student_id: str, email_par: str) -> None:
    with Session(engine) as session:
        existing_student = session.query(Student).filter_by(id=UUID(student_id)).first()
        if existing_student:
            return

        student = Student(
            id=UUID(student_id),
            hashed_password="hashedpassword123",
            number=random.randint(10000, 99999),
            email=email_par,
            name="mirco",
            surname="alessandrini",
        )
        session.add(student)
        session.commit()


def create_private_group(group_id: str, student_id: str) -> None:

            group_payload = {
                "id": group_id,
                "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
                "description": "A test group description",
                "category": "Test Category",
                "type": "Private",
                "creator_id": student_id,
            }
            response = client.post("/groups/create", json=group_payload)
            return response.json()

def test_join_private_group_success() -> None:

    creator_id = "508fc8f8-8e52-4adb-aa02-e9c9c41a0b19"
    group_id = "12345678-1234-5678-1234-567812345679"
    user_id = "b94e5917-ddbf-4fef-969d-fb67f78d0bd7"

    create_student(creator_id, "teststudenta1@example.com")
    create_private_group(group_id, creator_id)
    create_student(user_id, "teststudenta2@example.com")

    # User joins the private group
    response = client.post(
        "/groups/join_private_group",
        params={
            "student_id": user_id,
            "group_id": group_id,
        },
    )
    assert response.status_code in [200, 400]

    response = client.get(
        f"/groups/{group_id}/requests",
        params={"group_id": group_id},
    )
    assert response.status_code == 200

    requests_data = response.json()

    join_request = next(
        (req for req in requests_data if req["student_id"] == user_id), None
    )
    assert join_request is not None, f"Join request not found. Requests data: {requests_data}"
    assert join_request["status"] == "PENDING"

    approve_path = f"/requests/{join_request['id']}/approve"

    approve_response = client.post(approve_path)
    assert approve_response.status_code == 200


    response = client.get(
        f"/groups/{group_id}/requests",
        params={"group_id": group_id},
    )
    assert response.status_code == 200

    requests_data = response.json()
    join_request = next(
        (req for req in requests_data if req["student_id"] == user_id), None
    )
    assert join_request["status"] == "APPROVED"




