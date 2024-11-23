import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class BaseTest:
    @pytest.fixture
    def base_page(self, driver: webdriver.Chrome):
        self.wait = WebDriverWait(driver, 10)
        return driver
