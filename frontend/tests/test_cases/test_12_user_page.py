import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.user_page import UserPage
from tests.test_cases.base_test import BaseTest

class TestUserPage(BaseTest):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.UserPage = UserPage(self.driver)
        self.UserPage.load()

    def tearDown(self):
        self.driver.quit()

    def test_viewing_user_page_without_profile_image(self):
        name, surname, number, email, user_type = self.UserPage.get_user_details()
        profile_image = self.UserPage.get_profile_image()

        self.assertEqual(name, "John")
        self.assertEqual(surname, "Doe")
        self.assertEqual(number, "12345")
        self.assertEqual(email, "john.doe@example.com")
        self.assertEqual(user_type, "Admin")
        self.assertIn("placeholder.png", profile_image)

    def test_uploading_profile_image(self):
        self.UserPage.upload_profile_image("/path/to/new/profile/image.png")
        profile_image = self.UserPage.get_profile_image()

        self.assertIn("new/profile/image.png", profile_image)

    def test_displaying_profile_image_across_application(self):
        self.UserPage.upload_profile_image("/path/to/new/profile/image.png")
        self.UserPage.load()  # Reload the page to simulate navigation

        profile_image = self.UserPage.get_profile_image()
        self.assertIn("new/profile/image.png", profile_image)

    def test_error_during_image_upload(self):
        self.UserPage.upload_profile_image("/path/to/invalid/image.png")
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "error-message"))
        ).text

        self.assertEqual(error_message, "Upload failed. Please try again.")

if __name__ == "__main__":
    unittest.main()