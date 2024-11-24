from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
