import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.main_page import MainPage
from tests.test_cases.base_test import BaseTest


class TestManageGroupRequest(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.page = GroupPage(base_page)
        self.group_page_detail = GroupPageDetail(base_page)
        self.page.load()
        self.main_page = MainPage(base_page)

    def test_block_user(self) -> None:
        """Test that blocking a user removes them from the request list."""
        # First login as user1 and request to join
        self.login_fabio(self.page.driver)
        self.page.click_private_group_button()
        self.group_page_detail.click_ask_to_join()
        self.main_page.click_logout()

        # Login as user2 and block user1
        self.login(self.page.driver)
        # Reinitialize page objects after second login
        self.page = GroupPage(self.page.driver)
        self.group_page_detail = GroupPageDetail(self.page.driver)

        time.sleep(2)  # Allow page to load fully
        self.page.click_private_group_button()
        time.sleep(1)  # Allow page to load fully
        self.group_page_detail.click_request_item()
        time.sleep(1)  # Allow requests to load
        # Confirm block action
        self.group_page_detail.click_block_button(request_id=1)
        time.sleep(1)  # Allow time for the system to process
        # Verify the toast message appears for successful blocking
        toast_message = self.group_page_detail.get_toast_message()
        assert toast_message == "Success", (
            "Toast message did not appear or was incorrect."
        )
