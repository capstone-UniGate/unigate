from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls
from tests.pages.base_page import BasePage


class GroupPage(BasePage):
    URL = Urls.GROUP_PAGE
    # Locators using standard CSS selectors
    PAGE_HEADING = (By.CSS_SELECTOR, "h1")
    GROUP_CARDS = (By.CSS_SELECTOR, ".grid > div")

    def __init__(self, driver: webdriver.Chrome) -> None:
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def load(self) -> bool:
        try:
            self.driver.get(Urls.GROUP_PAGE)
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

    def click_button(self, group_card: WebElement) -> None:
        group_button = group_card.find_element(By.ID, "details")
        coordinates = group_button.location_once_scrolled_into_view
        self.driver.execute_script(
            "window.scrollTo({}, {});".format(coordinates["x"], coordinates["y"])
        )
        group_button.click()

    def is_page_loaded(self) -> bool:
        try:
            return (
                self.driver.execute_script("return document.readyState") == "complete"  # type: ignore
            )
        except Exception:  # noqa: BLE001
            return False

    def click_create_group(self) -> None:
        # Option 1: Wait for element to be clickable
        button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[data-testid='create-group-button']")
            )
        )
        button.click()

    def click_viwe_derails_group(self) -> None:
        # Option 1: Wait for element to be clickable
        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > main:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button:nth-child(1)",
                )
            )
        )
        button.click()

    def click_fabio_private_group_button(self) -> None:
        # Option 1: Wait for element to be clickable
        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//body//div[@id='__nuxt']//div[@class='p-4']//div[@class='p-4']//div[2]//div[1]//div[2]//button[1]",
                )
            )
        )
        button.click()

    def click_group_button(self) -> None:
        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4']//div[1]//div[1]//div[2]//button[1]",
                )
            )
        )
        button.click()

    def click_private_group_button(self) -> None:
        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[8]//div[1]//div[2]//button[1]",
                )
            )
        )
        button.click()

    def click_private_group_mimmo_button(self) -> None:
        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[6]//div[1]//div[2]//button[1]",
                )
            )
        )
        button.click()
