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

    def test_edit_photo_error(self) -> None:
        self.page.click_edit_button()
        try:
            self.page.change_profile_image("empy_path")
        except InvalidArgumentException as e:
            assert "File not found" in str(e)
        # time.sleep(1)
        # toast_message = self.page.get_toast_message()
        # assert (toast_message == "Error"), "Toast message did not appear or was correct."
