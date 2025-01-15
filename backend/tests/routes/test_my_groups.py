from fastapi.testclient import TestClient
from unigate.main import app

client: TestClient = TestClient(app)

test_student_password = "testpassword"


def authenticate_user(username="S1234567") -> dict:
    login_payload = {
        "username": username,
        "password": test_student_password,
    }

    response = client.post("/auth/login", data=login_payload)

    assert response.status_code == 200, (
        f"Failed to authenticate user: {response.json()}"
    )
    return response.json()


def test_my_groups_empty() -> None:
    token_data = authenticate_user(username="S4820312")
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    groups_list = client.get("/students/groups", headers=headers)
    groups_list_json = (groups_list.json())["groups"]
    assert isinstance(groups_list_json, list)
    assert groups_list_json == []


def test_my_groups() -> None:
    token_data = authenticate_user(username="S6015033")
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    groups_list = client.get("/students/groups", headers=headers)
    groups_list_json = (groups_list.json())["groups"]
    assert isinstance(groups_list_json, list)
    assert len(groups_list_json) == 2
