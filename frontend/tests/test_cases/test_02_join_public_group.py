import time

import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.test_cases.base_test import BaseTest


class TestGroupCreate(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login(base_page)
        self.page = GroupPage(base_page)
        self.page.load()

    def test_join_group_toast(self) -> None:
        """Test that clicking join button shows a toast message."""
        # Load the group details page
        group_card = (self.page.get_group_cards())[0]
        self.page.click_button(group_card)
        group_page_detail = GroupPageDetail(self.page.driver)

        time.sleep(1)
        # Click the button
        group_page_detail.click_join()
        # Small wait to allow alert to appear
