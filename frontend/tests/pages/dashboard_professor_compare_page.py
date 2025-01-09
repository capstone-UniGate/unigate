
from selenium.webdriver.common.by import By

from tests.constants import Urls

from .base_page import BasePage


class DashboardProfessorComparePage(BasePage):

    def navigate(self) -> None:
        self.driver.get(Urls.COMPARE_PAGE)

    def get_course_name_card(self) -> str:
        course_name = self.driver.find_element(By.ID, "course_name_card").text
        return course_name.split("\n")[0]
    
    def get_table_data(self) -> dict:
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table.w-full.text-sm.border-collapse tbody tr")
        table_data = {}
        for row in rows:
            key = row.find_element(By.CSS_SELECTOR, "td.font-medium").text.strip(":")
            value = row.find_elements(By.CSS_SELECTOR, "td")[1].text
            table_data[key] = int(value) if value.isdigit() else value
        return table_data
