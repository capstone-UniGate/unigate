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

    def check_members_list(self, members_list: list[WebElement]) -> bool:
        # Iterate through the members and verify their names and profile pictures
        for member in members_list:
            # Find the name element inside the member element
            name_element = member.find_element(By.ID, "member_name")

            # Assert that the name is displayed
            if not name_element.is_displayed() or name_element.text != "":
                return False

            if not member.find_element(By.ID, "block_member").is_displayed():
                return False
        return True

    def block_member(self) -> None:
        member = self.get_members()[0]
        member.find_element(By.ID, "block_member").click()

    def check_no_members(self) -> bool:
        return (self.driver.find_element(By.ID, "no_members")).is_displayed()

    def click_blocked_tab(self) -> None:
        blocked_tab = self.driver.find_element(By.ID, "blocked_tab")
        blocked_tab.click()

    def get_blocked(self) -> list[WebElement]:
        return self.driver.find_elements(By.ID, "blocked_student")

    def unblock_member(self) -> None:
        member = self.get_blocked()[0]
        member.find_element(By.ID, "unblock_student").click()

    def check_no_blocked(self) -> bool:
        return (self.driver.find_element(By.ID, "no_blocked_users")).is_displayed()
