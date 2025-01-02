from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls


class UserPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = Urls.USER_PAGE
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        """Navigate to the user profile page."""
        self.driver.get(self.url)

    def get_user_details(self):
        """Retrieve the user's details."""
        name = self.driver.find_element(By.ID, "user-name").text
        surname = self.driver.find_element(By.ID, "user-surname").text
        number = self.driver.find_element(By.ID, "user-number").text
        email = self.driver.find_element(By.ID, "user-email").text
        user_type = self.driver.find_element(By.ID, "user-type").text
        return {
            "name": name,
            "surname": surname,
            "number": number,
            "email": email,
            "user_type": user_type,
        }

    def get_profile_image(self):
        """Get the profile image source URL."""
        return self.driver.find_element(By.ID, "profile-image").get_attribute("src")

    def upload_profile_image(self, image_path):
        """Upload a new profile image."""
        upload_button = self.driver.find_element(By.ID, "upload-button")
        upload_button.send_keys(image_path)
        self.wait.until(
            EC.presence_of_element_located((By.ID, "profile-image"))
        )

    def get_error_message(self):
        """Retrieve the error message during upload."""
        return self.driver.find_element(By.ID, "error-message").text

    def simulate_upload_error(self):
        """Simulate an error during image upload."""
        self.driver.execute_script("window.simulateUploadError = true;")

    def retry_upload(self, image_path):
        """Retry uploading the profile image."""
        upload_button = self.driver.find_element(By.ID, "retry-upload")
        upload_button.send_keys(image_path)
        self.wait.until(
            EC.presence_of_element_located((By.ID, "profile-image"))
        )
