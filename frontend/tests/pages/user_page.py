from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UserPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = "http://localhost:3000/user"

    def load(self):
        self.driver.get(self.url)

    def get_user_name(self):
        return self.driver.find_element(By.ID, "user-name").text

    def get_user_surname(self):
        return self.driver.find_element(By.ID, "user-surname").text

    def get_user_number(self):
        return self.driver.find_element(By.ID, "user-number").text

    def get_user_email(self):
        return self.driver.find_element(By.ID, "user-email").text

    def get_user_type(self):
        return self.driver.find_element(By.ID, "user-type").text

    def get_placeholder_image(self):
        return self.driver.find_element(By.ID, "placeholder-image").is_displayed()

    def click_edit_button(self):
        self.driver.find_element(By.ID, "edit-button").click()

    def upload_profile_image(self, image_path):
        upload_button = self.driver.find_element(By.ID, "upload-photo")
        upload_button.send_keys(image_path)

    def wait_for_image_upload(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "profile-image"))
        )

    def get_uploaded_image_url(self):
        return self.driver.find_element(By.ID, "profile-image").get_attribute("src")
