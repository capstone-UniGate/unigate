from fastapi.testclient import TestClient
from unigate.main import app

client = TestClient(app)

def test_student_non_existent(client: TestClient) -> None:
    r = client.post("/groups/join_public_group", params={"student_id": "11111111111111112111111111111111", "group_id": "11111111111111111111111111111111"})
    assert r.status_code == 200
    assert r.json() == "Either the group or the student don't exist"

def test_group_non_existant(client: TestClient) -> None:
    r = client.post("/groups/join_public_group", params={"student_id": "11111111111111111111111111111111", "group_id": "11111111111111111111211111111111"})
    assert r.status_code == 200
    assert r.json() == "Either the group or the student don't exist"

def test_double_enrolling(client: TestClient) -> None:
    r = client.post("/groups/join_public_group", params={"student_id": "33333333333333333333333333333333", "group_id": "11111111111111111111111111111111"})
    assert r.status_code == 200
    assert r.json() == "You are already enrolled in a team for the same course"

def test_already_joined(cliend: TestClient) -> None:
    r = client.post("/groups/join_public_group", params={"student_id": "33333333333333333333333333333333", "group_id": "33333333333333333333333333333333"})
    assert r.status_code == 409
    assert r.json() == {"detail":"Resource already exists"}

def test_valid_join(client: TestClient) -> None:
    r = client.post("/groups/join_public_group", params={"student_id": "44444444444444444444444444444444", "group_id": "33333333333333333333333333333333"})
    assert r.status_code == 200
    assert r.json() == "Insert successful"

test_student_non_existent(client=client)
test_group_non_existant(client=client)
test_double_enrolling(client=client)
test_valid_join(client=client)