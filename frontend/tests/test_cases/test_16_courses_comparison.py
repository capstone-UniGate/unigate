import pytest
from selenium import webdriver

from tests.pages.dashboard_professor_compare_page import DashboardProfessorComparePage
from tests.test_cases.base_test import BaseTest


class TestUserProfile(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login_professor(base_page)
        self.page = DashboardProfessorComparePage(base_page)
        self.page.navigate()

    def test_course_name(self) -> None:
        course_name = "Binary Analysis and secure coding"
        assert self.page.get_course_name_card() == course_name

    def test_table_data(self) -> None:
        expected_data = {
            "Avg members/group": 1,
            "Min members": 1,
            "Max members": 1,
            "Total members": 1,
            "Total groups": 1,
        }
        actual_data = self.page.get_table_data()
        print(f"Actual data retrieved from the webpage: {actual_data}")
        assert actual_data == expected_data, f"Expected {expected_data} but got {actual_data}"

    def test_fail_contains(self) -> None:
        self.login_lorenzo()
        self.page.navigate()
        assert self.page.

