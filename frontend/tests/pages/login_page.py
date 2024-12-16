import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls


class LoginPage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.URL = Urls.LOGIN_PAGE
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, "button.bg-blue-600")
        self.error_message = (By.CSS_SELECTOR, ".text-red-500")
        self.success_message = (By.CSS_SELECTOR, ".bg-blue-100")
        self.retry_button = (By.XPATH, '//button[text()="Retry"]')
        self.username_clear_button = (
            By.XPATH,
            '//button[@type="button" and @class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"]',
        )
        self.password_clear_button = (
            By.XPATH,
            '//button[@type="button" and @class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"]',
        )

    def navigate(self) -> None:
        self.driver.get(self.URL)

    def enter_username(self, username: str) -> None:
        time.sleep(1)  # Small delay of 1 second
        self.driver.find_element(*self.username_input).send_keys(username)

    def enter_password(self, password: str) -> None:
        time.sleep(1)  # Small delay of 1 second
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login(self) -> None:
        login_button = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-blue-600"))
        )
        login_button.click()

    def click_retry(self) -> None:
        self.driver.find_element(*self.retry_button).click()

    def clear_username(self) -> None:
        self.driver.find_element(*self.username_clear_button).click()

    def clear_password(self) -> None:
        self.driver.find_element(*self.password_clear_button).click()

    def get_error_message(self) -> str:
        return self.driver.find_element(*self.error_message).text

    def get_success_message(self) -> str:
        welcome_message = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), 'Welcome')]")
            )
        )
        return welcome_message.text

    def is_login_button_disabled(self) -> bool:
        return "disabled" in self.driver.find_element(*self.login_button).get_attribute(
            "class"
        )

    def is_username_empty(self) -> bool:
        username_field = self.driver.find_element(*self.username_input)
        return username_field.get_attribute("value") == ""

    def is_password_empty(self) -> bool:
        return not self.driver.find_element(*self.password_input).get_attribute("value")

    def navigate_to_restricted_page(self) -> str:
        self.driver.get(Urls.SEE_MY_GROUP)
        return self.driver.current_url

    def is_login_page(self) -> bool:
        return self.driver.current_url == Urls.LOGIN_PAGE

    def simulate_network_error(self) -> None:
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd(
            "Network.emulateNetworkConditions",
            {
                "offline": True,
                "latency": 0,
                "downloadThroughput": 0,
                "uploadThroughput": 0,
            },
        )

    def restore_network(self) -> None:
        self.driver.execute_cdp_cmd(
            "Network.emulateNetworkConditions",
            {
                "offline": False,
                "latency": 0,
                "downloadThroughput": -1,
                "uploadThroughput": -1,
            },
        )
