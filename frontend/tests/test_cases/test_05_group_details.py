from pytest import fixture
import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers
from tests.test_cases.base_test import BaseTest


class TestGroupDetails(BaseTest):
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

    @pytest.mark.usefixtures("setup")
    def test_group_details_for_non_member(self) -> None:
        """Test that a non-member student sees the correct details on a private group page."""

        self.page.click_group_button()
        # Assert: Verify the group description is displayed
        assert (
            self.group_page_detail.check_description()
        ), "Incorrect display of description"
        assert (
            self.group_page_detail.check_join()
        ), "Ask to join button not displayed"
        self.group_page_detail.click_members()
        # members_emails = self.group_page_members.get_members()

        # assert len(members_emails)==0, "Non-members can see members"

        # Assert: Verify the "Join" button is visible
    @pytest.mark.usefixtures("setup_fabio")
    def test_group_details_for_superstudent(self) -> None:
        """Test that a superstudent sees the group details with join requests on group page with group id 1."""
        self.page.click_group_button()
        # Assert: Verify the group description is displayed
        assert (
            self.group_page_detail.check_description()
        ), "Incorrect display of description"
        assert self.group_page_detail.check_leave(), "Leave button not displayed"
        self.group_page_detail.click_members()
