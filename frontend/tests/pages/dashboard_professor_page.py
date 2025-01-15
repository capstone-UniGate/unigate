import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls

from .base_page import BasePage


class DashboardProfessorPage(BasePage):
    COURSE_FIELD = (By.ID, "course")

    def navigate(self) -> None:
        self.driver.get(Urls.DASHBOARD_PAGE)
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.COURSE_FIELD)
        )

    def set_course_name(self, name: str) -> None:
        self.driver.find_element(By.ID, "course_input").send_keys(str(name))

    def select_filter(self, number: int) -> None:
        self.driver.find_element(By.ID, f"filter_{number}").click()

    def select_exame_date(self, number: int) -> None:
        self.driver.find_element(By.ID, f"data_{number}").click()

    def get_course_name_card(self) -> str:
        course_name = self.driver.find_element(By.ID, "course_name_card").text
        return course_name.split("\n")[0]

    def get_course_number_groups(self) -> str:
        role = self.driver.find_element(By.ID, "course_number_groups").text
        return role.split("Groups: ")[1].strip()

    def get_course_data(self, number: int) -> str:
        return self.driver.find_element(By.ID, f"course_data_{number}").text

    def get_course_avg_members_group(self) -> str:
        role = self.driver.find_element(By.ID, "course_avg_members_group").text
        return role.split("Average members per group: ")[1].strip()

    def get_course_number_active_groups(self) -> str:
        role = self.driver.find_element(By.ID, "course_number_active_groups").text
        return role.split("Number of Active Groups: ")[1].strip()

    def get_group_creation_chart(self) -> WebElement:
        return self.driver.find_element(By.ID, "group_creation_chart")

    def get_yearly_group_creation_table(self) -> WebElement:
        return self.driver.find_element(By.ID, "yearly_group_creation_chart")
