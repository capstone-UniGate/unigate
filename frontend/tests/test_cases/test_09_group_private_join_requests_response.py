import time

import pytest
from pytest import fixture
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.test_cases.base_test import BaseTest


class TestGroupPrivateJoinRequestsResponse(BaseTest):
    @fixture()
    def setup(self, driver: webdriver.Chrome) -> None:
        self.login(driver)
        self.page = GroupPage(driver)
        self.group_page_detail = GroupPageDetail(driver)
        self.page.load()

    @fixture()
    def setup_2(self, driver: webdriver.Chrome) -> None:
        self.login_fabio(driver)
        self.page = GroupPage(driver)
        self.group_page_detail = GroupPageDetail(driver)
        self.page.load()

    @pytest.mark.usefixtures("setup_2")
    def test_empty_list(self) -> None:
        group_card = (self.page.get_group_cards())[1]
        self.page.click_button(group_card)
        self.group_page_detail.click_manage()
        assert self.group_page_detail.check_no_reqs(), "There are requests"

    @pytest.mark.usefixtures("setup")
    def test_click_approve(self) -> None:
        group_card = (self.page.get_group_cards())[7]
        self.page.click_button(group_card)
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        self.group_page_detail.approve_request(0)
        time.sleep(0.2)
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        assert (
            self.group_page_detail.get_status(0) == "Status: APPROVED"
        ), "Request not approved"

    @pytest.mark.usefixtures("setup")
    def test_click_reject(self) -> None:
        group_card = (self.page.get_group_cards())[7]
        self.page.click_button(group_card)
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        self.group_page_detail.reject_request(0)
        time.sleep(0.2)
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        assert (
            self.group_page_detail.get_status(0) == "Status: REJECTED"
        ), "Request not rejected"

    @pytest.mark.usefixtures("setup")
    def test_click_block(self) -> None:
        group_card = (self.page.get_group_cards())[7]
        self.page.click_button(group_card)
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        self.group_page_detail.block_request(0)
        time.sleep(0.2)
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        assert (
            self.group_page_detail.get_status(0) == "Status: BLOCKED"
        ), "Request not blocked"
