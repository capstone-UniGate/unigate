from fastapi.testclient import TestClient
from unigate.main import app

client = TestClient(app)

def test_get_group_info(client: TestClient) -> None:
    r = client.post("/groups/get_group", params={"group_id": "11111111111111111111111111111111"})
    assert r.status_code == 200
    assert r.json() == {"type":"Public","name":"capstone4life","description":"ciao","id":"11111111-1111-1111-1111-111111111111","category":"capstone","creator_id":"11111111-1111-1111-1111-111111111111"}

def test_group_not_found(client: TestClient) -> None:
    r = client.post("/groups/get_group", params={"group_id": "11111111111111112111111111111111"})
    assert r.status_code == 404
    assert r.json() == {"detail":"Team not found."}

test_get_group_info(client=client)
test_group_not_found(client=client)