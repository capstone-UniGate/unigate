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


def create_and_login_student(student_id: str, number: int, mail: str) -> str:
    create_student(student_id, number, mail)
    # Use 'S' as the role character (assuming 'S' is a valid role)
    username = f"S{number}"
    token_resp = client.post("/auth/login", data={"username": username, "password": "hashedpassword123"})
    if token_resp.status_code == 200:
        return token_resp.json()["access_token"]
    return ""


def create_group(student_id: str, group_id: str) -> dict:
    token = create_and_login_student(student_id=student_id, number=12345, mail="teststudent")
    headers = {"Authorization": f"Bearer {token}"}
    group_payload = {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
    }
    response = client.post("/groups", json=group_payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {}


def join_group(student_id: str, group_id: str) -> dict:
    number = 99999
    mail = f"randommail{secrets.randbelow(100000)}"
    token = create_and_login_student(student_id, number, mail)
    if not token:
        return {}
    headers = {"Authorization": f"Bearer {token}"}
    join_resp = client.post(f"/groups/{group_id}/join", headers=headers)
    return join_resp.json() if join_resp.status_code == 200 else {}


def leave_group(student_id: str, group_id: str) -> dict:
    with Session(engine) as session:
        student = session.query(Student).filter_by(id=UUID(student_id)).first()
        if not student:
            return {}
        token_resp = client.post("/auth/login", data={"username": f"S{student.number}", "password": "hashedpassword123"})
        if token_resp.status_code != 200:
            return {}
        token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post(f"/groups/{group_id}/leave", headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        return resp.json()


def get_group_data(group_id: str) -> dict:
    resp = client.get(f"/groups/{group_id}")
    return resp


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
    group_data = create_group(student_id=student_id, group_id=group_id)
    assert "id" in group_data
    r = client.post(
        f"/groups/{group_id}/leave",
        params={
            "student_id": student_id2,
            "group_id": group_id,
        },
    )
    assert r.status_code == 404
    assert r.json() == {"detail": "Student not found."}


def test_valid_leave() -> None:
    group_data = create_group(student_id=student_id, group_id=group_id)
    assert "id" in group_data
    join_group(student_id=student_id, group_id=group_id)
    join_group(student_id=student_id2, group_id=group_id)

    before = get_group_data(group_id).json()
    count_before = len(before["students"])

    after_leave = leave_group(student_id=student_id2, group_id=group_id)
    assert "students" in after_leave
    assert len(after_leave["students"]) == count_before - 1
    assert not any(m["id"] == student_id2 for m in after_leave["students"])

    after = get_group_data(group_id).json()
    assert len(after["students"]) == count_before - 1


def test_valid_leave_no_members(client: TestClient) -> None:
    group_data = create_group(student_id=student_id, group_id=group_id)
    assert "id" in group_data
    join_group(student_id=student_id, group_id=group_id)

    result = leave_group(student_id=student_id, group_id=group_id)
    assert "students" in result
    assert len(result["students"]) == 0

    r = get_group_data(group_id)
    if r.status_code == 200:
        final_group = r.json()
        assert "students" in final_group
        assert len(final_group["students"]) == 0
    else:
        assert r.status_code == 404
        assert r.json() == {"detail": "Group not found."}