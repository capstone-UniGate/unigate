from fastapi.testclient import TestClient
from unigate.core.config import settings
from unigate.enums import Mode
from unigate.main import app

client = TestClient(app)

test_professor_username = "P1234567"
test_professor_password = "testpassword"


def authenticate_user(
    username=test_professor_username, password=test_professor_password
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


def fetch_professor_statistic_number_of_groups(course_name: str) -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/courses/{course_name}/number_of_groups", headers=headers)
    assert response.status_code == 200, f"Failed to fetch user data: {response.json()}"
    return response.json()

def fetch_professor_statistic_average_members(course_name: str) -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/courses/{course_name}/average_members", headers=headers)
    assert response.status_code == 200, f"Failed to fetch user data: {response.json()}"
    return response.json()

def fetch_professor_statistic_distribution(course_name: str) -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/courses/{course_name}/distribution", headers=headers)
    assert response.status_code == 200, f"Failed to fetch user data: {response.json()}"
    return response.json()

def fetch_professor_statistic_active(course_name: str, exam_date: str) -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/courses/{course_name}/active?exam_date={exam_date}", headers=headers)
    assert response.status_code == 200, f"Failed to fetch user data: {response.json()}"
    return response.json()



def test_verify_professor_statistic() -> None:
    professor_statistic = fetch_professor_statistic_number_of_groups("Capstone")
    assert professor_statistic["count"] == 2
    assert professor_statistic["groups"] == ["Test Private Group 4891185", "Test Public Group 5475593"]

def test_verify_professor_statistic_average_members() -> None:
    professor_statistic = fetch_professor_statistic_average_members("Capstone")
    assert professor_statistic["avg"] == 1
    assert professor_statistic["min"] == 1
    assert professor_statistic["max"] == 1
    expected_members = {
        "Test Private Group 4891185": 1,
        "Test Public Group 5475593": 1
    }
    assert professor_statistic["members"] == expected_members

def test_verify_professor_statistic_distribution() -> None:
    professor_statistic = fetch_professor_statistic_distribution("Capstone")
    assert professor_statistic["course_name"] == "Capstone"
    assert professor_statistic["total_groups"] == 2

    groups_info = professor_statistic["groups_info"]
    assert len(groups_info) == 2

    group_1 = groups_info[0]
    assert group_1["group_name"] == "Test Private Group 4891185"
    assert group_1["creation_date"] == "2025-01-06T00:00:00"
    assert group_1["exam_date"] == "2025-02-03"
    assert group_1["creator_name"] == "Fabio Fontana"
    assert group_1["super_students"] == ["Fabio Fontana"]

    group_2 = groups_info[1]
    assert group_2["group_name"] == "Test Public Group 5475593"
    assert group_2["creation_date"] == "2025-01-06T00:00:00"
    assert group_2["exam_date"] == "2025-02-03"
    assert group_2["creator_name"] == "Forough Majidi"
    assert group_2["super_students"] == ["Forough Majidi"]


def test_verify_professor_statistic_active() -> None:
    professor_statistic = fetch_professor_statistic_active("Capstone", "2025-02-03")
    assert professor_statistic["course_name"] == "Capstone"
    assert professor_statistic["total_students"] == 2
    expected_students = ["Fabio Fontana", "Forough Majidi"]
    assert professor_statistic["student_names"] == expected_students
