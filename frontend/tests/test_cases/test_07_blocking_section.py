import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers
from tests.pages.main_page import MainPage
from tests.test_cases.base_test import BaseTest


class TestBlockingSection(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.page = GroupPage(base_page)
        self.group_page_detail = GroupPageDetail(base_page)
        self.group_page_members = GroupPageMembers(base_page)
        self.page.load()
        self.main_page = MainPage(base_page)  # Add this line to define main_page

    def test_block_user(self) -> None:
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
        self.group_page_members = GroupPageMembers(self.page.driver)
        time.sleep(2)
        self.page.click_private_group_button()
        time.sleep(3)
        self.group_page_detail.click_manage()
        time.sleep(0.5)
        self.group_page_members.block_member()

    def test_unblock_user(self) -> None:
        self.page.click_private_group_button()

        self.group_page_detail.click_members()
        self.group_page_members.click_blocked_tab()
        self.group_page_members.unblock_member()
        time.sleep(0.5)
        assert self.group_page_members.check_no_blocked(), "User is still blocked"
