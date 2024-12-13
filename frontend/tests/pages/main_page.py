from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812

from tests.constants import Urls

from .base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver: webdriver.Chrome) -> None:
        super().__init__(driver)
        # Set the URL after initialization
        self.URL = (
            Urls.BASE_URL
        )  # or use a specific path like f"{Urls.BASE_URL}/dashboard"

    # Locators
    LOGOUT_BUTTON = (By.ID, "logout-button")

    def click_logout(self) -> None:
        """Click the logout button and wait for redirection"""
        logout_btn = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON))
        logout_btn.click()
