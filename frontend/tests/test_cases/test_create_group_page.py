import time

import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812

from tests.constants import TestData, Urls
from tests.pages.create_group_page import CreateGroupPage
from tests.test_cases.base_test import BaseTest


class TestGroupCreate(BaseTest):
    @pytest.fixture
    def page(self, base_page: webdriver.Chrome) -> CreateGroupPage:
        page = CreateGroupPage(base_page)
        page.navigate()
        return page

    def test_create_group_form(self, page: CreateGroupPage) -> None:
        page.fill_form(TestData.VALID_GROUP)
        page.click_create()
        self.wait.until(EC.url_to_be(url=Urls.GROUP_PAGE))

    def test_form_validation(self, page: CreateGroupPage) -> None:
        # Define expected validation messages
        time.sleep(1)
        expected_messages: dict[str, str | int] = {"required": "Required", "count": 5}

        page.click_create()
        error_messages = page.get_error_messages()

        # Type assertion to tell mypy that we know "required" key contains a string
        required_msg = expected_messages["required"]
        assert isinstance(required_msg, str)
        actual_required_count = error_messages.count(required_msg)
        assert (
            actual_required_count == expected_messages["count"]
        ), f"Expected {expected_messages['count']} 'Required' messages, but got {actual_required_count}. Messages: {error_messages}"

    def test_cancel_button(self, page: CreateGroupPage) -> None:
        time.sleep(1)
        page.click_cancel()
        self.wait.until(EC.url_to_be(url=Urls.GROUP_PAGE))
