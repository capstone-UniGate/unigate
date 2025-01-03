import os
import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException

from tests.pages.user_page import UserPage
from tests.test_cases.base_test import BaseTest


class TestUserProfile(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login(base_page)
        self.page = UserPage(base_page)
        self.page.navigate()

    def test_verify_user_profile(self) -> None:
        assert (
            self.page.get_user_name_and_surname() == "Test Name Test Surname"
        ), "Name and surname are wrong not displayed"
        assert (
            self.page.get_user_email() == "s1234567@studenti.unige.it"
        ), "Email is wrong not displayed"
        assert self.page.get_user_role() == "Student", "Role is wrong or not displayed"

    def test_edit_photo(self) -> None:
        relative_path_profile_image = "unigate/frontend/tests/test_cases/lorax.jpeg"
        project_root = (
            os.getcwd()
        )  # Assume that the test is execute at the root of the project
        path_without_last_two = os.path.dirname(
            os.path.dirname(project_root)
        )  # Remove the last two directories
        file_path_profile_image = os.path.join(
            path_without_last_two, relative_path_profile_image
        )  # Create the absolute path

        self.page.click_edit_button()
        self.page.change_profile_image(file_path_profile_image)
        time.sleep(1)
        toast_message = self.page.get_toast_message()
        assert (
            toast_message == "Success"
        ), "Toast message did not appear or was incorrect."

    def test_edit_photo_error(self) -> None:
        self.page.click_edit_button()
        try:
            self.page.change_profile_image("empy_path")
        except InvalidArgumentException as e:
            assert "File not found" in str(e)
        # time.sleep(1)
        # toast_message = self.page.get_toast_message()
        # assert (toast_message == "Error"), "Toast message did not appear or was correct."
