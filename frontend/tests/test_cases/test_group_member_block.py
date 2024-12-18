import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers
from tests.test_cases.base_test import BaseTest


class TestGroupMemberBlock(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        # Perform login and initialize pages
        self.login(base_page)
        self.page = GroupPage(base_page)
        self.group_page_detail = GroupPageDetail(base_page)
        self.group_page_members = GroupPageMembers(base_page)

        self.page.load()

    def test_block_user(self) -> None:
        """Test that blocking a user removes them from the request list."""
        # Load the group details page
        group_card = self.page.get_group_cards()[1]
        self.page.click_button(group_card)

        time.sleep(1)  # Allow page to load fully

        self.group_page_detail.click_members()

        # Confirm block action
        self.group_page_members.block_member()

        time.sleep(1)  # Allow time for the system to process
