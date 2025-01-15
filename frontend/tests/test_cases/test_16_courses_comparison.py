import pytest
from selenium import webdriver

from tests.pages.dashboard_professor_compare_page import DashboardProfessorComparePage
from tests.test_cases.base_test import BaseTest


class TestUserProfile(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.base_page = base_page
        self.page = DashboardProfessorComparePage(base_page)

    def login_and_navigate(self, login_method: callable) -> None:
        login_method(self.base_page)
        self.page.navigate()

    def test_course_name(self) -> None:
        self.login_and_navigate(self.login_professor)
        course_name = "Binary Analysis and secure coding"
        actual_course_name = self.page.get_course_name_card()
        assert actual_course_name == course_name, (
            f"Expected '{course_name}' but got '{actual_course_name}'"
        )

    def test_table_data(self) -> None:
        self.login_and_navigate(self.login_professor)
        expected_data = {
            "Avg members/group": 1,
            "Min members": 1,
            "Max members": 1,
            "Total members": 1,
            "Total groups": 1,
        }
        actual_data = self.page.get_table_data()
        assert actual_data == expected_data, (
            f"Expected {expected_data} but got {actual_data}"
        )

    def test_fail_contains(self) -> None:
        self.login_and_navigate(self.login_lorenzo)
        assert self.page.is_access_denied_image_present(), (
            "The 'Access Denied' image is not present on the page."
        )
