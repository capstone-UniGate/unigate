from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.base_page import BasePage
from tests.constants import Urls

class LoginPage(BasePage):
    # Define XPath constants
    USERNAME_XPATH = '//input[@id="username"]'
    PASSWORD_XPATH = '//input[@id="password"]'
    LOGIN_BUTTON_XPATH = '//button[normalize-space()="Login"]'
    ERROR_MESSAGE_XPATH = "//p[@class='text-red-500 text-sm mt-2']"

    def __init__(self, driver: webdriver.Chrome) -> None:
        """Initialize LoginPage and set URL from constants."""
        super().__init__(driver)
        self.URL = Urls.LOGIN_PAGE

    def load(self):
        """Load the login page."""
        self.driver.get(self.URL)

    def _get_element(self, xpath: str) -> WebElement:
        """General helper method to locate an element and wait for its presence."""
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def enter_text(self, xpath: str, text: str):
        """Helper method to enter text into input fields."""
        field = self._get_element(xpath)
        field.clear()
        field.send_keys(text)

    def enter_username(self, username: str):
        """Enter username into the username field."""
        self.enter_text(self.USERNAME_XPATH, username)

    def enter_password(self, password: str):
        """Enter password into the password field."""
        self.enter_text(self.PASSWORD_XPATH, password)

    def click_login_button(self):
        """Click the login button."""
        login_button = self._get_element(self.LOGIN_BUTTON_XPATH)
        login_button.click()

    def get_error_message(self) -> WebElement:
        """Get the error message displayed after failed login."""
        return self._get_element(self.ERROR_MESSAGE_XPATH)
    
    def get_login_button(self) -> WebElement:
        """Returns the login button element."""
        return self._get_element(self.LOGIN_BUTTON_XPATH)

    def is_element_displayed(self, xpath: str) -> bool:
        """Check if an element is displayed by its XPath."""
        try:
            element = self._get_element(xpath)
            return element.is_displayed()
        except:
            return False

    def is_login_button_disabled(self) -> bool:
        """Check if the login button is disabled."""
        login_button = self.get_login_button()
        return not login_button.is_enabled()
