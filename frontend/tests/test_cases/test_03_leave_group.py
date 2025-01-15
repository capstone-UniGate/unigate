import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers
from tests.test_cases.base_test import BaseTest


class TestLeaveGroup(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login(base_page)
        self.page = GroupPage(base_page)
        self.group_page_detail = GroupPageDetail(base_page)
        self.group_page_members = GroupPageMembers(base_page)
        self.page.load()

    def test_leave_group(self) -> None:
        # Load the group details page
        self.page.click_group_button()

        time.sleep(0.5)
        # Click the button
        self.group_page_detail.click_leave()
        # Small wait to allow alert to appear
        time.sleep(0.5)
        self.group_page_detail.click_members()
        members_emails = self.group_page_members.get_members_email()
        assert (
            any(x.text == "s1234567@studenti.unige.it" for x in members_emails) == 0
        ), "Student has not been removed"
