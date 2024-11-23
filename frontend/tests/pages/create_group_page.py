from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls

from .base_page import BasePage


class CreateGroupPage(BasePage):
    # URL
    URL = Urls.CREATE_GROUP_PAGE

    # Locators
    NAME_INPUT = (By.ID, "group-name-input")
    COURSE_SELECT = (By.ID, "course-select")
    PRIVACY_PUBLIC = (By.ID, "privacy-public")
    DESCRIPTION = (By.ID, "group-description")
    TAGS_INPUT = (By.ID, "tags-input")
    CREATE_BUTTON = (By.ID, "create-group-button")
    CANCEL_BUTTON = (By.ID, "cancel-button")
    FORM_MESSAGE = (By.CLASS_NAME, "form-message")
    SUGGESTIONS_LIST = (By.CLASS_NAME, "suggestions-list")
    SUGGESTION_ITEM = (By.CLASS_NAME, "suggestion-item")

    TAG = (By.CLASS_NAME, "tag")

    def navigate(self) -> None:
        self.driver.get(self.URL)

    def set_name(self, name: str) -> None:
        name_input = self.driver.find_element(*self.NAME_INPUT)
        name_input.send_keys(str(name))

    def select_course(self, course: str) -> None:
        course_select = self.driver.find_element(*self.COURSE_SELECT)
        course_select.click()
        course_select.send_keys(str(course))
        course_select.send_keys(Keys.RETURN)

    def set_privacy_public(self) -> None:
        privacy_public = self.driver.find_element(*self.PRIVACY_PUBLIC)
        privacy_public.click()

    def set_description(self, description: str) -> None:
        description_field = self.driver.find_element(*self.DESCRIPTION)
        description_field.send_keys(description)

    def add_tags(self, tags: list[str]) -> None:
        tags_input = self.driver.find_element(*self.TAGS_INPUT)
        for tag in tags:
            tags_input.send_keys(tag)
            tags_input.send_keys(Keys.RETURN)

    def click_create(self) -> None:
        create_button = self.driver.find_element(*self.CREATE_BUTTON)
        create_button.click()

    def click_cancel(self) -> None:
        cancel_button = self.driver.find_element(*self.CANCEL_BUTTON)
        cancel_button.click()

    def get_error_messages(self) -> list[str]:
        """Get all form validation error messages"""
        wait = WebDriverWait(self.driver, 10)
        # Wait for at least one error message to appear
        wait.until(lambda d: len(d.find_elements(By.TAG_NAME, "p")) > 0)

        # Get all error messages from p tags
        error_elements = self.driver.find_elements(By.TAG_NAME, "p")
        return [element.text for element in error_elements if element.text.strip()]

    def enter_tag_text(self, tag_text: str) -> None:
        tags_input = self.wait.until(ExpectedConditions.presence_of_element_located(self.TAGS_INPUT))
        tags_input.send_keys(tag_text)

    def get_tag_suggestions(self) -> list[str]:
        """Get the list of tag suggestions"""
        # Wait for suggestions list to be visible
        self.wait.until(ExpectedConditions.presence_of_element_located(self.SUGGESTIONS_LIST))
        # Get all suggestion items
        suggestion_elements = self.driver.find_elements(*self.SUGGESTION_ITEM)
        # Return the text of each suggestion
        return [element.text for element in suggestion_elements]

    def get_added_tags(self):
        return self.driver.find_elements(*self.TAG)

    def verify_success_toast(self) -> bool:
        toast = self.wait.until(
            ExpectedConditions.presence_of_element_located((By.CLASS_NAME, "toast-success"))
        )
        return "Group created successfully" in toast.text

    def fill_form(self, data: dict[str, str | list[str]]) -> None:
        """Fill the entire form with provided data"""
        self.select_course(str(data["course"]))
        self.set_name(str(data["name"]))
        self.set_privacy_public()
        self.set_description(str(data["description"]))
        self.add_tags(
            data["tags"] if isinstance(data["tags"], list) else [data["tags"]]
        )

    def verify_validation_messages(self, expected_messages: list[str]) -> bool:
        """Verify all expected validation messages are present"""
        actual_messages = self.get_error_messages()
        return all(msg in actual_messages for msg in expected_messages)
