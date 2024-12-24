from fastapi.testclient import TestClient
from unigate.main import app

client = TestClient(app)

# Constants
VALID_USERNAME = "S4989646"
VALID_PASSWORD = "testpassword"
INVALID_USERNAME = "invalid_user"
INVALID_PASSWORD = "wrongpassword"


def test_login_valid_credentials() -> None:
    """Test login with valid username and password."""
    response = client.post(
        "/auth/login", data={"username": VALID_USERNAME, "password": VALID_PASSWORD}
    )
    # assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    print(data)
    assert "access_token" in data, "Missing access token in the response."
    assert data["token_type"] == "bearer", "Incorrect token type."


def test_login_invalid_username() -> None:
    """Test login with an invalid username."""
    response = client.post(
        "/auth/login", data={"username": INVALID_USERNAME, "password": VALID_PASSWORD}
    )
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_login_invalid_password() -> None:
    """Test login with an invalid password."""
    response = client.post(
        "/auth/login", data={"username": VALID_USERNAME, "password": INVALID_PASSWORD}
    )
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_login_empty_username_and_password() -> None:
    """Test login with empty username and password fields."""
    response = client.post("/auth/login", data={"username": "", "password": ""})
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    data = response.json()
    assert "detail" in data, "Invalid username"


def test_login_missing_username() -> None:
    """Test login with missing username."""
    response = client.post("/auth/login", data={"password": VALID_PASSWORD})
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    data = response.json()
    assert "detail" in data, "Internal Server Error"


def test_login_missing_password() -> None:
    """Test login with missing password."""
    response = client.post("/auth/login", data={"username": VALID_USERNAME})
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    data = response.json()
    assert "detail" in data, "Incorrect username or password"
