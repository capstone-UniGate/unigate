
from selenium.webdriver.common.by import By

from tests.constants import Urls

from .base_page import BasePage


class DashboardProfessorComparePage(BasePage):

    def navigate(self) -> None:
        self.driver.get(Urls.COMPARE_PAGE)

    def get_course_name_card(self) -> str:
        course_name = self.driver.find_element(By.ID, "course_name_card").text
        return course_name.split("\n")[0]
