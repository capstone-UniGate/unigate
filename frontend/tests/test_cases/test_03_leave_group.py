import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers


class TestLeaveGroup:
    @pytest.fixture(autouse=True)
    def setup(self, driver: webdriver.Chrome) -> None:
        self.page = GroupPage(driver)
        self.group_page_detail = GroupPageDetail(driver)
        self.group_page_members = GroupPageMembers(driver)
        self.page.load()

    def test_leave_group(self) -> None:
        # Load the group details page
        group_card = (self.page.get_group_cards())[0]
        self.page.click_button(group_card)

        time.sleep(1)
        # Click the button
        self.group_page_detail.click_leave()
        # Small wait to allow alert to appear
        self.group_page_detail.click_members()
        members_emails = self.group_page_members.get_members_email()
        assert (
            any(x.text == "s1234567@studenti.unige.it" for x in members_emails) == 0
        ), "Student has not been removed"
