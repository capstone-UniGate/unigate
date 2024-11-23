from fastapi.testclient import TestClient


def test_get_groups(client: TestClient) -> None:
    r = client.get("http://localhost:8000/groups/get")
    assert r.status_code == 200
