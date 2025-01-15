import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.create_group_page import CreateGroupPage
from tests.test_cases.base_test import BaseTest


class TestGroupCreate(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        """Setup the test by logging in and navigating to the group creation page."""
        self.login(base_page)
        self.page = CreateGroupPage(base_page)
        self.page.navigate()
        time.sleep(0.5)

    def test_create_and_cancel_group(self) -> None:
        """Test creating a group and canceling the form."""
        # Fill in the group name
        name_input = self.page.get_group_name_input()
        name_input.send_keys("Test Group Name")

        # Fill in the course field
        course_input = self.page.get_course_input()
        course_input.send_keys("Test Course")
        time.sleep(1)  # Allow time for the dropdown to appear
        course_input.send_keys(Keys.DOWN)
        course_input.send_keys(Keys.ENTER)

        # Select an exam date if available
        exam_dropdown = self.page.get_exam_date_dropdown()
        if exam_dropdown.is_enabled():
            WebDriverWait(self.page.driver, 10).until(
                expected_conditions.element_to_be_clickable(exam_dropdown)
            ).click()
            options = self.page.get_exam_date_options()
            if len(options) > 1:
                options[1].click()  # Select the first available date

        # Select privacy type
        privacy_radio_public = self.page.get_privacy_radio_public()
        privacy_radio_public.click()

        # Fill in the description field
        description_input = self.page.get_description_input()
        description_input.send_keys("This is a test group description.")

        # Add tags
        tags_input = self.page.get_tags_input()
        tags_input.send_keys("Vue.js")
        tags_input.send_keys(Keys.ENTER)
        tags_input.send_keys("Web Development")
        tags_input.send_keys(Keys.ENTER)

        # Test cancel button
        cancel_button = self.page.get_cancel_button()
        cancel_button.click()
        assert WebDriverWait(self.page.driver, 10).until(
            expected_conditions.url_contains("/groups")
        ), "Cancel button did not redirect to the groups page."

    def test_create_group_submit(self) -> None:
        """Test that the form is successfully submitted to create a group."""
        # Fill in the group name
        name_input = self.page.get_group_name_input()
        name_input.send_keys("Test Group Name")

        # Fill in the course field
        course_input = self.page.get_course_input()
        course_input.send_keys("Test Course")
        time.sleep(1)  # Allow time for the dropdown to appear
        course_input.send_keys(Keys.DOWN)
        course_input.send_keys(Keys.ENTER)

        # Select an exam date if available
        exam_dropdown = self.page.get_exam_date_dropdown()
        if exam_dropdown.is_enabled():
            WebDriverWait(self.page.driver, 10).until(
                expected_conditions.element_to_be_clickable(exam_dropdown)
            ).click()
            options = self.page.get_exam_date_options()
            if len(options) > 1:
                options[1].click()  # Select the first available date

        # Select privacy type
        privacy_radio_public = self.page.get_privacy_radio_public()
        privacy_radio_public.click()

        # Fill in the description field
        description_input = self.page.get_description_input()
        description_input.send_keys("This is a test group description.")

        # Add tags
        tags_input = self.page.get_tags_input()
        tags_input.send_keys("Vue.js")
        tags_input.send_keys(Keys.ENTER)
        tags_input.send_keys("Web Development")
        tags_input.send_keys(Keys.ENTER)
        # Submit the form
        submit_button = self.page.get_submit_button()
        WebDriverWait(self.page.driver, 10).until(
            expected_conditions.element_to_be_clickable(submit_button)
        ).click()

        # Verify success toast message
        toast_message = self.page.get_toast_message()
        assert "Group created successfully!" in toast_message.text
