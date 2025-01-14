import pytest
from selenium import webdriver

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers
from tests.test_cases.base_test import BaseTest


class TestGroupDetails(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login(base_page)
        self.page = GroupPage(base_page)
        self.group_page_detail = GroupPageDetail(base_page)
        self.group_page_members = GroupPageMembers(base_page)
        self.page.load()

    def test_group_details_for_non_member(self) -> None:
        """Test that a non-member student sees the correct details on a private group page."""

        self.page.click_group_button()
        # Assert: Verify the group description is displayed
        assert (
            self.group_page_detail.check_description()
        ), "Incorrect display of description"
        assert self.group_page_detail.check_members_link(), "Members link not displayed"
        assert (
            self.group_page_detail.check_ask_join()
        ), "Ask to join button not displayed"
        self.group_page_detail.click_members()
        # members_emails = self.group_page_members.get_members()

        # assert len(members_emails)==0, "Non-members can see members"

        # Assert: Verify the "Join" button is visible

    def test_group_details_for_superstudent(self) -> None:
        """Test that a superstudent sees the group details with join requests on group page with group id 1."""
        group_card = (self.page.get_group_cards())[7]
        self.page.click_button(group_card)
        # Assert: Verify the group description is displayed
        assert (
            self.group_page_detail.check_description()
        ), "Incorrect display of description"
        assert self.group_page_detail.check_members_link(), "Members link not displayed"
        assert self.group_page_detail.check_leave(), "Leave button not displayed"
        assert self.group_page_detail.check_manage(), "Manage button not displayed"
        self.group_page_detail.click_members()
        members_list = self.group_page_members.get_members()

        assert len(members_list) > 0, "Superstudent can't see members"
        self.group_page_members.check_members_list(members_list=members_list)
