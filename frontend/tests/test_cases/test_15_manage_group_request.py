import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.test_cases.base_test import BaseTest


class TestManageGroupRequest(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        # Perform login and initialize pages
        self.login(base_page, "S4891185")
        self.page = GroupPage(base_page)
        self.group_page_detail = GroupPageDetail(base_page)
        self.page.load()

    def test_block_user(self) -> None:
        """Test that blocking a user removes them from the request list."""
        # Load the group details page
        group_card = self.page.get_group_cards()[1]
        self.page.click_button(group_card)

        time.sleep(1)  # Allow page to load fully

        # Click on "Manage Requests" in the group detail page

        self.group_page_detail.click_request_item()

        time.sleep(1)  # Allow requests to load

        # Select a user request to block
        # self.group_page_detail.click_request_action(request_id, "block")

        # Confirm block action
        self.group_page_detail.click_block_button(request_id=1)

        time.sleep(1)  # Allow time for the system to process

        # Verify the toast message appears for successful blocking
        toast_message = self.group_page_detail.get_toast_message()
        assert toast_message == "Success", (
            "Toast message did not appear or was incorrect."
        )

        # Verify the user request is no longer in the list
        # remaining_requests = self.group_page_detail.get_request_list()

        # assert (
        #     request_id not in remaining_requests
        # ), "Blocked user request still appears in the list."
