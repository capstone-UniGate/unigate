from fastapi.testclient import TestClient
from unigate.main import app

client: TestClient = TestClient(app)

test_student_username = "S1234567"
test_student_password = "testpassword"  # noqa:S105


def authenticate_user() -> dict:
    """Authenticate a test user and return the access token."""
    login_payload = {
        "username": test_student_username,
        "password": test_student_password,
    }

    response = client.post("/auth/login", data=login_payload)
    assert (
        response.status_code == 200
    ), f"Failed to authenticate user: {response.json()}"
    return response.json()


def test_get_group_number_valid() -> None:
    """Test group creation with valid data."""
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        "/courses/get_group_number?course_name=Test Course", headers=headers
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert data["count"] == 10, f"Expected 10, got {data['count']} instead"
    assert (
        data["course"]["name"] == "Test Course"
    ), f"Expected Test Course, got {data["Course"]["Name"]} instead"


def test_get_group_number_invalid() -> None:
    """Test group creation with valid data."""
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/courses/get_group_number?course_name=Test", headers=headers)
    assert (
        response.status_code == 404
    ), f"Expected status code 404, but got {response.status_code}"


def test_get_groups_course_valid() -> None:
    """Test group creation with valid data."""
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        "/courses/get_groups?course_name=Test Course", headers=headers
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert len(data) == 10, f"Expected 10, got {len(data)} instead"


def test_get_groups_course_invalid() -> None:
    """Test group creation with valid data."""
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/courses/get_groups?course_name=Test", headers=headers)
    assert (
        response.status_code == 404
    ), f"Expected status code 404, but got {response.status_code}"


def test_get_groups_exam_valid() -> None:
    """Test group creation with valid data."""
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        "/courses/get_groups_exams?course_name=Test Course&date=2025-01-01",
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert len(data) == 10, f"Expected 10, got {len(data)} instead"


def test_get_groups_exam_invalid_date() -> None:
    """Test group creation with valid data."""
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        "/courses/get_groups_exams?course_name=Test Course&date=1198-12-27",
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert len(data) == 0, f"Expected 0, got {len(data)} instead"


def test_get_groups_exam_invalid_course() -> None:
    """Test group creation with valid data."""
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        "/courses/get_groups_exams?course_name=Test&date=2024-12-27", headers=headers
    )
    assert (
        response.status_code == 404
    ), f"Expected status code 404, but got {response.status_code}"
