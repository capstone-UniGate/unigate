import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from tests.pages.group_page import GroupPage
from tests.pages.group_page_detail import GroupPageDetail
from tests.pages.group_page_members import GroupPageMembers
from tests.test_cases.base_test import BaseTest


class TestLogout(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login(base_page)
        self.page = GroupPage(base_page)
        self.group_page_detail = GroupPageDetail(base_page)
        self.group_page_members = GroupPageMembers(base_page)
        self.page.load()

    def test_group_details_for_non_member(self) -> None:
        """Test that a non-member student sees the correct details on a private group page."""

        group_card = (self.page.get_group_cards())[1]
        self.page.click_button(group_card)
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
        time.sleep(1)
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

        # Iterate through the members and verify their names and profile pictures
        for member in members_list:
            # Find the name element inside the member element
            name_element = member.find_element(By.ID, "member_name")

            # Assert that the name is displayed
            assert (
                name_element.is_displayed()
            ), f"Name of member {member.text} is not displayed."
            assert name_element.text != "", f"Member name is empty for {member.text}."

            # Optionally, check if the profile picture exists (if there's an avatar)
            # assert member.find_element(By.ID, "avatar").is_displayed(), "Profile picture is not displayed."
            assert member.find_element(
                By.ID, "block_member"
            ).is_displayed(), "Block member button is not displayed."
