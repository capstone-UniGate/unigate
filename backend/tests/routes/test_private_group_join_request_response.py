import secrets
import string
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session
from unigate.core.database import engine
from unigate.main import app
from unigate.models import Student

client = TestClient(app)
student_id = uuid.uuid4()
student_id2 = uuid.uuid4()
group_id = uuid.uuid4()


def create_student(student_id: uuid.UUID, email_par: str) -> None:
    with Session(engine) as session:
        existing_student = session.query(Student).filter_by(id=student_id).first()
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


def create_private_group(group_id: uuid.UUID, student_id: uuid.UUID) -> None:
    group_payload = {
        "id": str(group_id),
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Private",
        "creator_id": str(student_id),
    }
    response = client.post("/groups/create", json=group_payload)
    return response.json()


# Test cases
def test_create_request_success() -> None:
    create_student(student_id=student_id, email_par="ciao")
    create_student(student_id=student_id2, email_par="ciao2")
    create_private_group(group_id, student_id)

    response = client.post(
        "/groups/join_private_group",
        params={"student_id": student_id2, "group_id": group_id},
    )

    assert response.status_code == 200
    assert response.json() == "Join request submitted successfully"


def test_create_request_group_not_found() -> None:
    new_group_id = uuid.uuid4()

    response = client.post(
        "/groups/join_private_group",
        params={"student_id": student_id, "group_id": new_group_id},
    )

    assert response.status_code == 200
    assert response.json() == "Either the group or the student doesn't exist"


def test_create_request_already_exists() -> None:
    response = client.post(
        "/groups/join_private_group",
        params={"student_id": student_id2, "group_id": group_id},
    )

    assert response.status_code == 400


def test_get_all_requests_for_group() -> None:
    response = client.get("/groups/" + str(group_id) + "/requests")
    data = response.json()
    assert len(data) == 1
    assert data[0]["student_id"] == str(student_id2)
    assert data[0]["group_id"] == str(group_id)
    assert data[0]["status"] == "PENDING"


def test_reject_request_success() -> None:
    response = client.get("/groups/" + str(group_id) + "/requests")
    request_id = (response.json())[0]["id"]

    second_response = client.post(
        "/requests/" + str(request_id) + "/reject", params={"request_id": request_id}
    )
    assert second_response.status_code == 200

    third_response = client.get("/groups/" + str(group_id) + "/requests")
    assert (third_response.json())[0]["status"] == "REJECTED"


def test_reject_request_already_rejected() -> None:
    response = client.get("/groups/" + str(group_id) + "/requests")
    request_id = (response.json())[0]["id"]
    assert (response.json())[0]["status"] == "REJECTED"

    second_response = client.post(
        "/requests/" + str(request_id) + "/reject", params={"request_id": request_id}
    )
    assert second_response.status_code == 400
    assert second_response.json() == {"detail": "Request is already rejected."}


def test_approve_request_success() -> None:
    student_id3 = uuid.uuid4()
    create_student(student_id=student_id3, email_par="ciao3")

    client.post(
        "/groups/join_private_group",
        params={"student_id": student_id3, "group_id": group_id},
    )

    response = client.get("/groups/" + str(group_id) + "/requests")
    request_id = (response.json())[1]["id"]

    second_response = client.post(
        "/requests/" + str(request_id) + "/approve", params={"request_id": request_id}
    )
    assert second_response.status_code == 200

    third_response = client.get("/groups/" + str(group_id) + "/requests")
    assert (third_response.json())[1]["status"] == "APPROVED"


def test_approve_request_already_approved() -> None:
    response = client.get("/groups/" + str(group_id) + "/requests")
    request_id = (response.json())[1]["id"]
    assert (response.json())[1]["status"] == "APPROVED"

    second_response = client.post(
        "/requests/" + str(request_id) + "/approve", params={"request_id": request_id}
    )
    assert second_response.status_code == 400
    assert second_response.json() == {"detail": "Request is already approved."}


def test_request_not_existing() -> None:
    request_id = uuid.uuid4()

    second_response = client.post(
        "/requests/" + str(request_id) + "/approve", params={"request_id": request_id}
    )
    assert second_response.status_code == 404
    assert second_response.json() == {
        "detail": "Request not found or does not belong to the group."
    }
