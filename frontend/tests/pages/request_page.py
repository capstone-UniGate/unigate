from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.base_page import BasePage


class RequestPage(BasePage):
    # URL = Urls.JOIN_REQUESTS_PAGE
    # Locators using standard CSS selectors
    PAGE_HEADING = (By.CSS_SELECTOR, "h1")
    LIST_REQUESTS = (By.CSS_SELECTOR, "<ul role='list'")
    APPROVE_BUTTON = (By.CLASS_NAME, "bg-green-500")
    REJECT_BUTTON = (By.CLASS_NAME, "bg-red-500")
    FIRST_REQUEST = (By.XPATH, "//ul[@role='list']/li[1]")

    def __init__(self, driver: webdriver.Chrome) -> None:
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def is_heading_visible(self) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.PAGE_HEADING)
            ).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_requests_list(self) -> list[WebElement]:
        try:
            self.wait.until(EC.presence_of_element_located(self.LIST_REQUESTS))
            return self.driver.find_elements(*self.LIST_REQUESTS)
        except (TimeoutException, NoSuchElementException):
            return []

    def is_page_loaded(self) -> bool:
        try:
            return (
                self.driver.execute_script("return document.readyState") == "complete"  # type: ignore
            )
        except Exception:  # noqa: BLE001
            return False

    def select_request(self) -> WebElement:
        return self.driver.find_element(*self.FIRST_REQUEST)

    def click_approve(self, child: WebElement) -> None:
        button = child.find_element(*self.APPROVE_BUTTON)
        button.click()

    def click_reject(self, child: WebElement) -> None:
        button = child.find_element(*self.REJECT_BUTTON)
        button.click()
