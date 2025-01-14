from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from tests.constants import Urls

from .base_page import BasePage


class CreateGroupPage(BasePage):
    # URL
    URL = Urls.CREATE_GROUP_PAGE

    # Locators
    NAME_INPUT = (By.ID, "radix-v-0-0-form-item")
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

    PAGE_READY_INDICATOR = (
        CREATE_BUTTON  # Indicatore che conferma il caricamento della pagina
    )

    def navigate(self) -> None:
        """Naviga alla pagina specificata e attende il caricamento."""
        self.driver.get(Urls.CREATE_GROUP_PAGE)
        self.wait_for_page_load()

    def wait_for_page_load(self) -> None:
        """Aspetta che la pagina sia completamente caricata."""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PAGE_READY_INDICATOR)
        )

    def set_name(self, name: str) -> None:
        self.wait_for_page_load()
        name_input = self.driver.find_element(*self.NAME_INPUT)
        name_input.send_keys(str(name))

    def select_course(self, course: str) -> None:
        self.wait_for_page_load()
        course_select = self.driver.find_element(*self.COURSE_SELECT)
        course_select.click()
        course_select.send_keys(str(course))
        course_select.send_keys(Keys.RETURN)

    def set_privacy_public(self) -> None:
        self.wait_for_page_load()
        privacy_public = self.driver.find_element(*self.PRIVACY_PUBLIC)
        privacy_public.click()

    def set_description(self, description: str) -> None:
        self.wait_for_page_load()
        description_field = self.driver.find_element(*self.DESCRIPTION)
        description_field.send_keys(description)

    def add_tags(self, tags: list[str]) -> None:
        self.wait_for_page_load()
        tags_input = self.driver.find_element(*self.TAGS_INPUT)
        for tag in tags:
            tags_input.send_keys(tag)
            tags_input.send_keys(Keys.RETURN)

    def click_create(self) -> None:
        self.wait_for_page_load()
        create_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CREATE_BUTTON)
        )
        create_button.send_keys(Keys.ENTER)

    def click_cancel(self) -> None:
        self.wait_for_page_load()
        cancel_button = self.driver.find_element(*self.CANCEL_BUTTON)
        cancel_button.click()

    def get_error_messages(self) -> list[str]:
        """Get all form validation error messages"""
        self.wait_for_page_load()
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(By.TAG_NAME, "p")) > 0
        )
        error_elements = self.driver.find_elements(By.TAG_NAME, "p")
        return [element.text for element in error_elements if element.text.strip()]

    def enter_tag_text(self, tag_text: str) -> None:
        self.wait_for_page_load()
        tags_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.TAGS_INPUT)
        )
        tags_input.send_keys(tag_text)

    def get_tag_suggestions(self) -> list[str]:
        """Get the list of tag suggestions"""
        self.wait_for_page_load()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SUGGESTIONS_LIST)
        )
        suggestion_elements = self.driver.find_elements(*self.SUGGESTION_ITEM)
        return [element.text for element in suggestion_elements]

    def get_added_tags(self) -> list[WebElement]:
        self.wait_for_page_load()
        return self.driver.find_elements(*self.TAG)

    def verify_success_toast(self) -> bool:
        self.wait_for_page_load()
        toast = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "toast-success"))
        )
        return "Group created successfully" in toast.text

    def fill_form(self, data: dict[str, str | list[str]]) -> None:
        """Fill the entire form with provided data"""
        self.wait_for_page_load()
        self.set_name(str(data["name"]))
        self.select_course(str(data["course"]))
        self.set_privacy_public()
        self.set_description(str(data["description"]))
        self.add_tags(
            data["tags"] if isinstance(data["tags"], list) else [data["tags"]]
        )

    def verify_validation_messages(self, expected_messages: list[str]) -> bool:
        self.wait_for_page_load()
        """Verify all expected validation messages are present"""
        actual_messages = self.get_error_messages()
        return all(msg in actual_messages for msg in expected_messages)
    

    def enter_text(self, selector: str, text: str):
        element = self.driver.find_element(By.XPATH, selector)
        element.clear()
        element.send_keys(text)

        # Helper function to select a dropdown option
    def select_option(self, selector: str, value: str):
        dropdown = Select(self.driver.find_element(By.XPATH, selector))
        dropdown.select_by_visible_text(value)

    def enter_course_name(self, course_name: str):
        self.enter_text("//input[@placeholder='Enter Course Name']", course_name)

    def enter_group_name(self, group_name: str):
        self.enter_text("//input[@id='radix-v-0-0-form-item']", group_name)
        
    def enter_group_name(self, course_name: str):
        self.enter_text(self.SELECTORS["#radix-v-0-0-form-item"], course_name)

    def select_exam_date(self, date: str):
        self.select_option("//select[@id='examDate']", date)


    def select_public_filter(self):
        self.select_option("is_public_dropdown", "Public")

    def select_private_filter(self):
        self.select_option("is_public_dropdown", "Private")
    