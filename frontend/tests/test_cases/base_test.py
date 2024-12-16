import time

import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.login_page import LoginPage


class BaseTest:
    @pytest.fixture
    def base_page(self, driver: webdriver.Chrome) -> webdriver.Chrome:
        self.wait = WebDriverWait(driver, 10)
        return driver

    def login(self, driver: webdriver.Chrome) -> None:
        self.page = LoginPage(driver)
        self.page.load()
        self.page.login("S1234567", "testpassword")
        time.sleep(1)
        cookies = driver.get_cookies()
        bearer_token = None

        for cookie in cookies:
            if cookie["name"] == "access_token":
                bearer_token = cookie
                break
        driver.add_cookie(bearer_token)
