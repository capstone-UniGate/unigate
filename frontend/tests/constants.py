from typing import ClassVar


class TestData:
    VALID_GROUP: ClassVar[dict[str, str | list[str]]] = {
        "name": "Test Group",
        "course": "course1",
        "description": "This is a test group description that meets the minimum length requirement.",
        "tags": ["JavaScript", "Vue.js"],
    }

    VALIDATION_MESSAGES: ClassVar[dict[str, str]] = {
        "required": "Required",
        "name_length": "Name must be at least 2 characters long",
        "description_length": "The description is too short",
        "tags_required": "Please add at least one tag",
    }


class Urls:
    BASE_URL = "http://localhost:3000"
    GROUP_PAGE = f"{BASE_URL}/groups"
    SEE_MY_GROUP = f"{GROUP_PAGE}/see-my-group"
    CREATE_GROUP_PAGE = f"{GROUP_PAGE}/create"
    JOIN_REQUESTS_PAGE = f"{GROUP_PAGE}/1/requests"
