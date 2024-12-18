import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.test_cases.base_test import BaseTest


class TestPrivateGroupJoinRequest(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, driver: webdriver.Chrome) -> None:
        self.login_fabio(driver)
        self.page = GroupPage(driver)
        self.group_page_detail = GroupPageDetail(driver)
        self.page.load()

    def test_join_group_toast(self) -> None:
        # Load the group details page
        group_card = (self.page.get_group_cards())[7]
        self.page.click_button(group_card)
        time.sleep(1)
        # Click the button
        self.group_page_detail.click_ask_to_join()
        time.sleep(1)
        assert self.group_page_detail.check_req()
        # Small wait to allow alert to appear
