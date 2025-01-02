import pytest
from selenium import webdriver

from tests.pages.user_page import UserPage
from tests.test_cases.base_test import BaseTest


class TestUserProfile(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        """Setup fixture for logging in and navigating to the user page."""
        self.login(base_page)  # Login setup
        self.page = UserPage(base_page)
        self.page.load()

    def test_view_profile_without_image(self) -> None:
        """Test viewing the user profile without a profile image."""
        user_details = self.page.get_user_details()
        assert user_details["name"], "Name not displayed"
        assert user_details["surname"], "Surname not displayed"
        assert user_details["number"], "Student number not displayed"
        assert user_details["email"], "Email not displayed"
        assert user_details["user_type"], "User type not displayed"
        profile_image = self.page.get_profile_image()
        assert "placeholder" in profile_image, "Placeholder image not displayed"

    def test_upload_profile_image(self) -> None:
        """Test uploading a profile image."""
        image_path = "/path/to/test_image.jpg"
        self.page.upload_profile_image(image_path)
        updated_image = self.page.get_profile_image()
        assert updated_image and "test_image.jpg" in updated_image, "Profile image not updated"

    def test_display_image_across_application(self) -> None:
        """Test that the uploaded profile image is displayed across the application."""
        image_path = "/path/to/test_image.jpg"
        self.page.upload_profile_image(image_path)
        updated_image = self.page.get_profile_image()
        # Add navigation to sections and checks for the image, similar to `check_image_in_comments` and `check_image_in_topbar`

    def test_error_during_image_upload(self) -> None:
        """Test error handling during profile image upload."""
        self.page.simulate_upload_error()
        error_message = self.page.get_error_message()
        assert error_message == "Failed to update profile photo", "Error message not displayed correctly"
        self.page.retry_upload("/path/to/test_image.jpg")
        updated_image = self.page.get_profile_image()
        assert updated_image and "test_image.jpg" in updated_image, "Retry upload failed"
