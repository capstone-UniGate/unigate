import time

import pytest
from selenium import webdriver

from tests.pages.group_page_detail import GroupPageDetail
from tests.test_cases.base_test import BaseTest


class TestPrivateGroupJoinRequest(BaseTest):
    @pytest.fixture
    def page(self, base_page: webdriver.Chrome) -> GroupPageDetail:
        page = GroupPageDetail(base_page, group_id="4")
        page.navigate()
        return page

    def test_join_group_toast(self, page: GroupPageDetail) -> None:
        # Load the group details page
        page.load()
        time.sleep(1)
        # Click the button
        page.click_join()
        # Small wait to allow alert to appear
