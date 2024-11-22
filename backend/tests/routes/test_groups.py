from unittest.mock import MagicMock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unigate.main import app
from unigate.models import Group, GroupType

client: TestClient = TestClient(app)


@pytest.fixture
def mock_session() -> MagicMock:
    session: MagicMock = MagicMock(spec=Session)
    return session


# These tests, for now, assume the existence of a valid creator_id in the `students` table
# This is because the `students` table is not mocked in this test suite
# You have to ensure that the creator_id: 12345678-1234-5678-1234-567812345678 exists in the `students` table before running these tests


@pytest.fixture
def valid_group_payload() -> dict[str, str]:
    return {
        "name": "Test Group",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": "12345678-1234-5678-1234-567812345678",
    }


def test_create_group_success(
    mock_session: MagicMock, valid_group_payload: dict[str, str]
) -> None:
    response = client.post("/groups/create", json=valid_group_payload)
    assert response.status_code == 201
    data: dict[str, str] = response.json()
    assert data["name"] == valid_group_payload["name"]
    assert data["description"] == valid_group_payload["description"]
    assert data["category"] == valid_group_payload["category"]
    assert data["type"] == valid_group_payload["type"]
    assert data["creator_id"] == valid_group_payload["creator_id"]


def test_create_group_duplicate_name(
    mock_session: MagicMock, valid_group_payload: dict[str, str]
) -> None:
    # Create a mock `Group` instance matching the payload
    mock_group = Group(
        id=UUID("12345678-1234-5678-1234-567812345678"),  # UUID for id
        name=valid_group_payload["name"],
        description=valid_group_payload["description"],
        category=valid_group_payload["category"],
        type=GroupType(valid_group_payload["type"]),  # Convert string to GroupType
        creator_id=UUID(valid_group_payload["creator_id"]),  # Convert string to UUID
    )
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        mock_group
    )

    response = client.post("/groups/create", json=valid_group_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Group with this name already exists."


def test_create_group_invalid_type(valid_group_payload: dict[str, str]) -> None:
    invalid_payload: dict[str, str] = valid_group_payload.copy()
    invalid_payload["type"] = "InvalidType"
    invalid_payload["name"] = "NewName1"
    response = client.post("/groups/create", json=invalid_payload)
    assert response.status_code == 400
    assert "Invalid group type" in response.json()["detail"]


def test_create_group_non_existing_creator_id(
    mock_session: MagicMock, valid_group_payload: dict[str, str]
) -> None:
    # Ensure the creator_id remains a valid UUID string
    valid_group_payload["creator_id"] = str(
        UUID("12345678-1234-5678-1234-567812345679")
    )
    valid_group_payload["name"] = "NewName3"
    # Simulate a non-existing creator_id
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    response = client.post("/groups/create", json=valid_group_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Creator ID does not exist in students table."
