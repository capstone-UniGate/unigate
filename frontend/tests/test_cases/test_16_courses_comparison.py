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
