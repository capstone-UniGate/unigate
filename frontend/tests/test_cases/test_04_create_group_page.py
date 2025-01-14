import pytest
from selenium import webdriver
from tests.pages.create_group_page import CreateGroupPage
from tests.test_cases.base_test import BaseTest


class TestGroupCreate(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login(base_page)
        self.page = CreateGroupPage(base_page)
        self.page.navigate()

    def test_create_group(self) -> None:
        self.page.enter_group_name("Test")
        self.page.enter_course_name("Test Course")
        self.page.select_exam_date("2025-01-01")
        self.page.select_public_filter()

        
    