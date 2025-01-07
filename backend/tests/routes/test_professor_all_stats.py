from fastapi.testclient import TestClient
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


def fetch_all_stats() -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/courses/all_stats", headers=headers)
    assert (
        response.status_code == 200
    ), f"Failed to fetch course stats: {response.json()}"
    return response.json()


def get_all_course_names() -> list[str]:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/courses/names_courses", headers=headers)
    assert (
        response.status_code == 200
    ), f"Failed to fetch course names: {response.json()}"
    return response.json()


def modular_test(
    course_name: str,
    expected_value: str | int,
    argument_to_test: str,
    exam_date: str = None,
) -> None:
    stats = fetch_all_stats()

    assert course_name in stats, f"Course {course_name} not found in stats"

    course_details = stats[course_name]

    assert len(course_details) > 0, f"No exams found for the course {course_name}"

    if exam_date:
        matching_group = next(
            (group for group in course_details if group["exam_date"] == exam_date), None
        )
        assert matching_group, f"Exam on {exam_date} not found for course {course_name}"
    else:
        matching_group = course_details[0]

    assert (
        argument_to_test in matching_group
    ), f"Argument {argument_to_test} not found in course details"

    value = matching_group[argument_to_test]
    assert value == expected_value, f"Incorrect: {value}. Expected: {expected_value}"


def test_all_stats_courses_present() -> None:
    stats = fetch_all_stats()
    course_names = get_all_course_names()
    for course_name in course_names:
        assert course_name in stats, f"Course {course_name} not present in stats"


def test_exam_date() -> None:
    assert modular_test("Capstone", "2025-02-03", "exam_date", "2025-02-03") is None


def test_average_members() -> None:
    modular_test("Capstone", 1, "average_members", "2025-02-03")


def test_min_members() -> None:
    modular_test("Capstone", 1, "min_members", "2025-02-03")


def test_max_members() -> None:
    modular_test("Capstone", 1, "max_members")


def test_total_members() -> None:
    modular_test("Binary Analysis and secure coding", 2, "total_members", "2025-01-08")


def test_total_groups() -> None:
    modular_test("Binary Analysis and secure coding", 2, "total_groups", "2025-01-08")


# def test_exam_date_not_found() -> None:
#    try:
#        modular_test("Capstone", "2024-02-04", "exam_date", "2024-02-04")
#    except AssertionError as e:
#        assert "Exam on 2024-02-04 not found for course Capstone" in str(e)
