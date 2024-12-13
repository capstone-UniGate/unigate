from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.URL = ""

    def load(self) -> None:
        """Load the page using the URL"""
        if not self.URL:
            raise ValueError("URL is not set")
        self.driver.get(self.URL)
