from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls

from .base_page import BasePage


class CreateGroupPage(BasePage):
    def navigate(self) -> None:
        """Navigate to the group creation page and wait for it to load."""
        self.driver.get(Urls.CREATE_GROUP_PAGE)

    def get_group_name_input(self) -> WebElement:
        return self.driver.find_element(By.ID, "course_name")

    def get_course_input(self) -> WebElement:
        return self.driver.find_element(
            By.XPATH, "//input[@placeholder='Enter Course Name']"
        )

    def get_exam_date_dropdown(self) -> WebElement:
        return self.driver.find_element(By.ID, "examDate")

    def get_exam_date_options(self) -> list[WebElement]:
        return self.driver.find_elements(By.TAG_NAME, "option")

    def get_privacy_radio_public(self) -> WebElement:
        return self.driver.find_element(By.XPATH, "//input[@value='Public']")

    def get_description_input(self) -> WebElement:
        return self.driver.find_element(
            By.XPATH, "//textarea[@placeholder='Describe your group']"
        )

    def get_tags_input(self) -> WebElement:
        return self.driver.find_element(By.XPATH, "//input[@placeholder='Add tags...']")

    def get_submit_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH, "//button[text()='Create']")

    def get_toast_message(self) -> WebElement:
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@class='text-sm opacity-90']")
            )
        )

    def get_cancel_button(self) -> WebElement:
        return self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Cancel']"
        )