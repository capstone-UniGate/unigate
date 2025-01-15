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

    def test_set_course_name2(self) -> None:
        course_name = "Capstone"
        self.page.set_course_name(course_name)
        assert self.page.get_course_name_card() == course_name

    def test_get_course_number_groups(self) -> None:
        self.page.set_course_name("Capstone")
        assert self.page.get_course_number_groups() == "2"

    def test_get_course_avg_members_group(self) -> None:
        self.page.set_course_name("Capstone")
        assert self.page.get_course_avg_members_group() == "1"

    def test_get_course_number_active_groups(self) -> None:
        self.page.set_course_name("Capstone")
        assert self.page.get_course_number_active_groups() == "0"

    def test_get_group_creation_chart(self) -> None:
        self.page.set_course_name("Capstone")
        self.page.select_filter(1)
        assert self.page.get_group_creation_chart() is not None, (
            "Group creation chart is not rendered"
        )

    def test_get_yearly_group_creation_table(self) -> None:
        self.page.set_course_name("Capstone")
        self.page.select_filter(1)
        assert self.page.get_yearly_group_creation_table() is not None, (
            "Yearly group creation chart is not rendered"
        )
