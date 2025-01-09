import secrets
import string
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select
from unigate.core.database import engine
from unigate.main import app
from unigate.models import Student

client = TestClient(app)

test_student_username = "S1234567"
test_student_password = "testpassword"
student_id = uuid.uuid4()
student_id2 = uuid.uuid4()
group_id = uuid.uuid4()


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


def create_student(student_id: uuid.UUID, email_par: str) -> None:
    with Session(engine) as session:
        existing_student = session.exec(
            select(Student).where(Student.id == student_id)
        ).first()
        if existing_student:
            return

        student = Student(
            id=student_id,
            hashed_password="hashedpassword123",  # noqa: S106
            number=secrets.choice(range(10000, 99999)),
            email=email_par,
            name="mirco",
            surname="alessandrini",
        )
        session.add(student)
        session.commit()


def create_group(student_id: uuid.UUID, group_id: uuid.UUID) -> dict:
    # Authenticate the user to get the token
    token_data = authenticate_user()
    token = token_data["access_token"]

    # Authorization headers
    headers = {"Authorization": f"Bearer {token}"}

    course = client.get("/courses").json()[0]
    # Group payload
    group_payload = {
        "id": str(group_id),
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",  # Adjust as needed
        "course_name": course["name"],
        "exam_date": course["exams"][0]["date"],
    }

    # Call the API to create the group
    response = client.post("/groups", json=group_payload, headers=headers)

    # Ensure the group creation was successful
    assert response.status_code == 200, f"Group creation failed: {response.json()}"
    return response.json()


def test_create_group_success() -> None:
    create_student(student_id=student_id, email_par="test1@example.com")
    group_data = create_group(student_id=student_id, group_id=group_id)

    assert "id" in group_data, f"Expected 'id' in group_data: {group_data}"
    assert group_data["name"].startswith("TestGroup"), "Group name format mismatch"


def test_create_group_failure_unauthenticated() -> None:
    # No authentication headers
    group_payload = {
        "id": str(group_id),
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
    }

    response = client.post("/groups", json=group_payload)
    assert (
        response.status_code == 401
    ), f"Expected 401 Unauthorized, got {response.status_code}"


def test_create_group_already_exists() -> None:
    create_student(student_id=student_id, email_par="test2@example.com")
    create_group(student_id=student_id, group_id=group_id)

    # Try creating the same group again
    try:
        create_group(student_id=student_id, group_id=group_id)
    except AssertionError as e:
        assert "Group creation failed" in str(
            e
        ), "Group creation did not fail as expected"


def test_join_group_not_found() -> None:
    new_group_id = uuid.uuid4()

    token_data = authenticate_user()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = client.post(f"/groups/{new_group_id}/join", headers=headers)
    assert response.status_code == 404, f"Expected 404, got: {response.status_code}"
    assert response.json() == {"detail": "Group not found."}


def test_leave_group_success() -> None:
    # Authenticate second student
    token_data = authenticate_user()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    groups_list = client.get("/groups", headers=headers)
    group_id = groups_list.json()[0]["id"]
    # Join group
    client.post(f"/groups/{group_id}/join", headers=headers)
    leaver_id = client.get("/students/me", headers=headers).json()["id"]

    # Leave group
    response = client.post(f"/groups/{group_id}/leave", headers=headers)
    students = (response.json())["students"]
    assert response.status_code == 200, f"Unexpected: {response.json()}"

    assert not any(
        student["id"] == leaver_id for student in students
    ), f"Leaver {leaver_id} found in group students list"
