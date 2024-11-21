from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .base_page import (
    EC,
    BasePage,
    By,
    NoSuchElementException,
    TimeoutException,
    WebDriverWait,
)


class GroupPage(BasePage):
    URL = "http://localhost:3000/group"

    # Locators using standard CSS selectors
    PAGE_HEADING = (By.CSS_SELECTOR, "h1")
    GROUP_CARDS = (By.CSS_SELECTOR, ".grid > div")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def load(self) -> bool:
        try:
            self.driver.get(self.URL)
        except Exception:  # noqa: BLE001
            return False
        return True

    def is_heading_visible(self) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.PAGE_HEADING)
            ).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_group_cards(self) -> list[WebElement]:
        try:
            self.wait.until(EC.presence_of_element_located(self.GROUP_CARDS))
            return self.driver.find_elements(*self.GROUP_CARDS)
        except (TimeoutException, NoSuchElementException):
            return []

    def is_page_loaded(self) -> bool:
        try:
            return (
                self.driver.execute_script("return document.readyState") == "complete"
            )
        except Exception:  # noqa: BLE001
            return False
