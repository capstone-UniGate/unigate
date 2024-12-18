import secrets
import string
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unigate.core.database import engine
from unigate.main import app
from unigate.models import Student

client = TestClient(app)

student_id = "12745678-1234-5678-1234-567812345678"
group_id = "12375678-1234-5678-1234-567812345677"
student_id2 = "12345678-1234-5778-1234-567812345678"


@pytest.fixture
def mock_session() -> MagicMock:
    session: MagicMock = MagicMock(spec=Session)
    return session


def create_student(student_id: str, number: int, mail: str) -> None:
    with Session(engine) as session:
        existing_student = session.query(Student).filter_by(id=UUID(student_id)).first()
        if existing_student:
            return
        student = Student(
            id=UUID(student_id),
            hashed_password="hashedpassword123",
            number=number,
            email=mail + "@example.com",
            name="Test",
            surname="Student",
        )
        session.add(student)
        session.commit()


def create_group(student_id: str, group_id: str) -> dict[str, str]:
    group_payload = {
        "id": group_id,
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": student_id,
    }
    response = client.post("/groups/create", json=group_payload)
    return response.json()


def test_group_non_existant() -> None:
    create_student(student_id=student_id, number=12347, mail="testsdstudent")
    r = client.post(
        "/groups/" + group_id + "/leave",
        params={
            "student_id": student_id,
            "group_id": group_id,
        },
    )
    assert r.status_code == 404
    assert r.json() == {"detail": "Group not found."}


def test_student_non_existent() -> None:
    create_group(student_id=student_id, group_id=group_id)
    r = client.post(
        "/groups/" + group_id + "/leave",
        params={
            "student_id": student_id,
            "group_id": group_id,
        },
    )
    assert r.status_code == 404
    assert r.json() == {"detail": "Student not found."}


def test_valid_leave() -> None:
    create_student(student_id=student_id2, number=12349, mail="testsstudent")
    client.post(
        "/groups/join_public_group",
        params={
            "student_id": student_id,
            "group_id": group_id,
        },
    )
    client.post(
        "/groups/join_public_group",
        params={
            "student_id": student_id2,
            "group_id": group_id,
        },
    )

    group_json = client.get("/groups/" + group_id)
    original_group = group_json.json()
    original_count = len(original_group["students"])

    response = client.post(
        "/groups/" + group_id + "/leave",
        params={
            "group_id": group_id,
            "student_id": student_id2,
        },
    )
    assert response.status_code == 200
    left_group = response.json()
    assert len(left_group["students"]) == original_count - 1
    assert all(member["id"] != student_id2 for member in left_group["students"])

    r = client.get("/groups/" + group_id)
    assert r.status_code == 200
    updated_group = r.json()
    # The group should still exist, with one less member
    assert len(updated_group["students"]) == len(original_group["students"]) - 1


def test_valid_leave_no_members(client: TestClient) -> None:
    # Join the group first (to have one member)
    create_student(student_id=student_id, number=12350, mail="testnostudent")
    create_group(student_id=student_id, group_id=group_id)
    client.post(
        "/groups/join_public_group",
        params={
            "student_id": student_id,
            "group_id": group_id,
        },
    )

    # Now leave the group as the only member
    response = client.post(
        "/groups/" + group_id + "/leave",
        params={
            "student_id": student_id,
            "group_id": group_id,
        },
    )
    assert response.status_code == 200
    # After leaving, the code currently still returns the updated group (empty students)
    empty_group = response.json()
    assert len(empty_group["students"]) == 0

    # Group should still exist (not deleted by the code)
    r = client.get("/groups/" + group_id)
    assert r.status_code == 200
    final_group = r.json()
    # Group exists with zero members
    assert len(final_group["students"]) == 0
