import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls
from tests.pages.login_page import LoginPage


class BaseTest:
    @pytest.fixture(autouse=True)
    def base_page(self, driver: webdriver.Chrome) -> webdriver.Chrome:
        self.wait = WebDriverWait(driver, 10)
        return driver

    def login(self, driver: webdriver.Chrome) -> None:
        self.page = LoginPage(driver)
        self.page.navigate()
        self.page.login("S1234567", "testpassword")
        self.wait.until(EC.url_to_be(url=Urls.GROUP_PAGE))
