from selenium import webdriver


class BasePage:
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
