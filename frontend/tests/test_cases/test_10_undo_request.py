import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.test_cases.base_test import BaseTest


class TestUndoJoinRequest(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, driver: webdriver.Chrome) -> None:
        self.login_lorenzo(driver)
        self.page = GroupPage(driver)
        self.group_page_detail = GroupPageDetail(driver)
        self.page.load()

    def test_undo_join_toast(self) -> None:
        # Load the group details page
        self.page.click_private_group_button()
        time.sleep(1)
        # Click the button
        self.group_page_detail.click_ask_to_join()
        time.sleep(1)
        assert self.group_page_detail.check_req()
        time.sleep(1)
        self.group_page_detail.click_undo_request()
        time.sleep(1)
        assert self.group_page_detail.check_ask_join()
