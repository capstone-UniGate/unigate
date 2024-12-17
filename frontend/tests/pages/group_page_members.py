from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class GroupPageMembers(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 1000)

    def get_members_email(self) -> list[WebElement]:
        return self.driver.find_elements(By.ID, "member_email")

    def get_members(self) -> list[WebElement]:
        return self.driver.find_elements(By.ID, "member")
