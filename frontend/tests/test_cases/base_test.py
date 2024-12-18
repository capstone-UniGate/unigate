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
        self.login_page = LoginPage(driver)
        self.login_page.navigate()
        self.login_page.login("S1234567", "testpassword")
        self.wait.until(EC.url_to_be(url=Urls.GROUP_PAGE))

    def login_fabio(self, driver: webdriver.Chrome) -> None:
        self.login_page = LoginPage(driver)
        self.login_page.navigate()
        self.login_page.login("S4891185", "testpassword")
        self.wait.until(EC.url_to_be(url=Urls.GROUP_PAGE))

    def login_lorenzo(self, driver: webdriver.Chrome) -> None:
        self.login_page = LoginPage(driver)
        self.login_page.navigate()
        self.login_page.login("S4989646", "testpassword")
        self.wait.until(EC.url_to_be(url=Urls.GROUP_PAGE))

    def login_mimmo(self, driver: webdriver.Chrome) -> None:
        self.login_page = LoginPage(driver)
        self.login_page.navigate()
        self.login_page.login("S5806782", "testpassword")
        self.wait.until(EC.url_to_be(url=Urls.GROUP_PAGE))
