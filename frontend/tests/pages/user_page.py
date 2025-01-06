import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls

from .base_page import BasePage


class UserPage(BasePage):
    EDIT_BUTTON = (By.ID, "edit-button")

    def navigate(self) -> None:
        self.driver.get(Urls.USER_PAGE)
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.EDIT_BUTTON)
        )

    def get_user_name_and_surname(self) -> str:
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user-name-surname"))
            )
            return element.text
        except Exception as e:
            print(f"Error while fetching name and surname: {e}")
            return ""

    def get_user_number(self) -> str:
        return self.driver.find_element(By.ID, "user-number").text

    def get_user_email(self) -> str:
        email = self.driver.find_element(By.ID, "Email").text
        return email.split("Email: ")[1].strip()

    def get_user_role(self) -> str:
        role = self.driver.find_element(By.ID, "Role").text
        return role.split("Role: ")[1].strip()

    # def get_image(self) -> None:
    # return #self.driver.find_element(By.ID, "placeholder-image").is_displayed()

    def click_edit_button(self) -> None:
        self.driver.find_element(By.ID, "edit-button").click()

    def change_profile_image(self, image_path: str) -> None:
        # self.driver.find_element(By.ID, "change-photo-click").click()
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(image_path)

    def get_toast_message(self) -> str:
        return (self.get_toast()).text.split("\n")[0]

    def get_toast(self) -> WebElement:
        return self.driver.find_element(
            By.CSS_SELECTOR, '[data-state="open"][data-swipe-direction="right"]'
        )

    # def get_uploaded_image_url(self):
    #    return self.driver.find_element(By.ID, "profile-image").get_attribute("src")
