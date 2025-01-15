import time

import pytest
from pytest import fixture
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers
from tests.pages.main_page import MainPage
from tests.test_cases.base_test import BaseTest


class TestGroupPrivateJoinRequestsResponse(BaseTest):
    @fixture()
    def setup(self, driver: webdriver.Chrome) -> None:
        self.login(driver)
        self.page = GroupPage(driver)
        self.group_page_detail = GroupPageDetail(driver)
        self.group_page_members = GroupPageMembers(driver)
        self.page.load()

    @fixture()
    def setup_fabio(self, driver: webdriver.Chrome) -> None:
        self.login_fabio(driver)
        self.page = GroupPage(driver)
        self.group_page_detail = GroupPageDetail(driver)
        self.page.load()

    @fixture()
    def setup_mimmo(self, driver: webdriver.Chrome) -> None:
        self.login_mimmo(driver)
        self.page = GroupPage(driver)
        self.group_page_detail = GroupPageDetail(driver)
        self.group_page_members = GroupPageMembers(driver)
        self.main_page = MainPage(driver)
        self.page.load()
        time.sleep(2)
        self.page.click_private_group_button()
        time.sleep(0.2)
        self.group_page_detail.click_leave()
        time.sleep(0.2)
        self.main_page.click_logout()
        time.sleep(0.2)
        self.login(driver)
        # self.page.load()

    @fixture()
    def setup_lorenzo(self, driver: webdriver.Chrome) -> None:
        self.login_lorenzo(driver)
        self.page = GroupPage(driver)
        self.group_page_detail = GroupPageDetail(driver)
        self.group_page_members = GroupPageMembers(driver)
        self.main_page = MainPage(driver)
        self.page.load()
        time.sleep(2)
        self.page.click_private_group_button()
        time.sleep(0.2)
        self.group_page_detail.click_ask_to_join()
        time.sleep(0.2)
        self.main_page.click_logout()
        time.sleep(0.2)
        self.login(driver)
        # self.page.load()

    @pytest.mark.usefixtures("setup_fabio")
    def test_empty_list(self) -> None:
        self.page.click_fabio_private_group_button()
        self.group_page_detail.click_manage()
        assert self.group_page_detail.check_no_reqs(), "There are requests"

    @pytest.mark.usefixtures("setup")
    def test_click_approve(self) -> None:
        self.page.click_private_group_button()
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        self.group_page_detail.approve_request(0)
        time.sleep(0.2)
        self.group_page_detail.click_members()
        members_emails = self.group_page_members.get_members_email()
        assert (
            any(x.text == "s4891185@studenti.unige.it" for x in members_emails) == 1
        ), "Student has not been inserted"

    @pytest.mark.usefixtures("setup_mimmo")
    def test_click_reject(self) -> None:
        self.page.click_private_group_mimmo_button()
        self.group_page_detail.click_manage()
        time.sleep(0.2)
        self.group_page_detail.reject_request(0)
        time.sleep(0.2)
        self.group_page_detail.click_members()
        members_emails = self.group_page_members.get_members_email()
        assert (
            any(x.text == "s5806782@studenti.unige.it" for x in members_emails) == 0
        ), "Student has been inserted"

    # @pytest.mark.usefixtures("setup_lorenzo")
    # def test_click_block(self) -> None:
    #     self.page.click_private_group_button()
    #     self.group_page_detail.click_manage()
    #     time.sleep(0.2)
    #     self.group_page_detail.block_request(0)
    #     time.sleep(0.2)
    #     self.group_page_detail.click_members()
    #     time.sleep(0.2)
    #     self.group_page_members.click_blocked_tab()
    #     blocked_emails = self.group_page_members.get_blocked_emails()
    #     assert (
    #         any(x.text == "s4989646@studenti.unige.it" for x in blocked_emails) == 1
    #     ), "Student has not been blocked"
