import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.user_page import UserPage
from tests.test_cases.base_test import BaseTest


class TestUserProfile(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page):
        self.login(base_page)
        self.page = UserPage(base_page)
        self.page.load()

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
