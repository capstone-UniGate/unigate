import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers
from tests.pages.main_page import MainPage
from tests.test_cases.base_test import BaseTest


class TestGroupMemberBlock(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.page = GroupPage(base_page)
        self.group_page_detail = GroupPageDetail(base_page)
        self.group_page_members = GroupPageMembers(base_page)

        self.page.load()
        self.main_page = MainPage(base_page)

    def test_block_user(self) -> None:
        """Test that blocking a user removes them from the request list."""
        # Load the group details page
        # First login as user1 and request to join
        self.login(self.page.driver)
        self.page = GroupPage(self.page.driver)
        self.group_page_detail = GroupPageDetail(self.page.driver)
        self.group_page_members = GroupPageMembers(self.page.driver)
        time.sleep(1)
        self.page.click_fabio_private_group_button()
        self.group_page_detail.click_ask_to_join()
        self.main_page.click_logout()

        self.login_fabio(self.page.driver)
        # Reinitialize page objects after second login
        self.page = GroupPage(self.page.driver)
        self.group_page_detail = GroupPageDetail(self.page.driver)
        self.group_page_members = GroupPageMembers(self.page.driver)
        self.page.click_fabio_private_group_button()
        time.sleep(1)  # Allow page to load fully
        self.group_page_detail.click_manage()
        time.sleep(1)  # Allow page to load fully
        self.group_page_members.approve_button()
        self.group_page_detail.click_members()
        time.sleep(1)  # Allow page to load fully
        self.group_page_members.block_member_inside_group()
