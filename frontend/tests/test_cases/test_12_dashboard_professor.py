import pytest
from selenium import webdriver

from tests.pages.dashboard_professor_page import DashboardProfessorPage
from tests.test_cases.base_test import BaseTest


class TestUserProfile(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login_professor(base_page)
        self.page = DashboardProfessorPage(base_page)
        self.page.navigate()

    def test_set_course_name(self) -> None:
        course_name = "Binary Analysis and secure coding"
        self.page.set_course_name(course_name)
        assert self.page.get_course_name_card() == course_name

    def test_set_course_name2(self) -> None:
        course_name = "Capstone"
        self.page.set_course_name(course_name)
        assert self.page.get_course_name_card() == course_name

    def test_select_filter(self) -> None:
        self.page.set_course_name("Cap")
        self.page.select_filter(1)
        assert self.page.get_course_name_card() == "Capstone"

    def test_select_exame_date(self) -> None:
        self.page.set_course_name("Capstone")
        self.page.select_exame_date(1)
        assert self.page.get_course_data(1) == "2025-02-03"

    def test_get_course_number_groups(self) -> None:
        self.page.set_course_name("Capstone")
        assert self.page.get_course_number_groups() == "2"
