import time

import pytest
from selenium import webdriver

from tests.constants import TestData
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
        self.page.click_edit_button()
        self.page.change_profile_image(TestData.IMAGE_PROFILE_TO_CHANGE_PATH)
        time.sleep(1)
        toast_message = self.page.get_toast_message()
        assert (
            toast_message == "Success"
        ), "Toast message did not appear or was incorrect."

        # assert self.page.get_image(), "Image not displayed"

    """
    def test_view_profile_without_image(self):
        WebDriverWait(self.page.driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        assert self.page.get_user_name() != "", "Name not displayed"
        assert self.page.get_user_surname() != "", "Surname not displayed"
        assert self.page.get_user_number() != "", "Student number not displayed"
        assert self.page.get_user_email() != "", "Email not displayed"
        assert self.page.get_user_type() != "", "User type not displayed"
        assert self.page.get_placeholder_image(), "Placeholder image not displayed"

    def test_upload_profile_image(self):
        image_path = "https://github.com/radix-vue.png"
        assert os.path.exists(image_path), "Test image does not exist"

        self.page.click_edit_button()
        self.page.upload_profile_image(image_path)
        self.page.wait_for_image_upload()
        uploaded_image_url = self.page.get_uploaded_image_url()
        assert uploaded_image_url is not None, "Profile image not updated"

    def test_display_image_across_application(self):
        image_path = "https://github.com/radix-vue.png"
        assert os.path.exists(image_path), "Test image does not exist"

        self.page.click_edit_button()
        self.page.upload_profile_image(image_path)
        self.page.wait_for_image_upload()
        uploaded_image_url = self.page.get_uploaded_image_url()
        assert uploaded_image_url is not None, "Profile image not updated"

    def test_error_during_image_upload(self):
        self.page.upload_profile_image("/invalid/path/to/image.jpg")
        error_message = self.page.get_error_message()
        assert error_message == "Failed to update profile photo", "Error message not displayed correctly"
    """
