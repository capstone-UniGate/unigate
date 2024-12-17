import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers
from tests.test_cases.base_test import BaseTest


class TestBlockingSection(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login(base_page)
        self.page = GroupPage(base_page)
        self.group_page_detail = GroupPageDetail(base_page)
        self.group_page_members = GroupPageMembers(base_page)
        self.page.load()

    def test_block_user(self) -> None:
        group_card = (self.page.get_group_cards())[7]
        self.page.click_button(group_card)
        self.group_page_detail.click_members()
        self.group_page_members.block_member()
        assert self.group_page_members.check_no_members(), "User is still there"
        self.group_page_members.click_blocked_tab()
        time.sleep(0.5)
        assert len(self.group_page_members.get_blocked()) > 0, "User is not blocked"

    def test_unblock_user(self) -> None:
        group_card = (self.page.get_group_cards())[7]
        self.page.click_button(group_card)
        self.group_page_detail.click_members()
        self.group_page_members.click_blocked_tab()
        self.group_page_members.unblock_member()
        time.sleep(0.5)
        assert self.group_page_members.check_no_blocked(), "User is still blocked"
