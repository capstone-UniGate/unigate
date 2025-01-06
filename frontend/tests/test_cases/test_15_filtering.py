import pytest
from selenium import webdriver

from tests.pages.group_filters_page import GroupFiltersPage
from tests.test_cases.base_test import BaseTest


class TestGroupFilters(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, base_page: webdriver.Chrome) -> None:
        self.login(base_page)
        self.page = GroupFiltersPage(base_page)

    def test_apply_single_filter(self) -> None:
        """Test applying a single filter (e.g., course) and checking results."""
        self.page.toggle_filters()
        self.page.enter_course("Test Course")
        self.page.select_public_filter()
        self.page.click_apply_filters()

    def test_apply_multiple_filters(self) -> None:
        """Test applying multiple filters (e.g., course, date, type) and checking results."""
        self.page.toggle_filters()
        self.page.enter_course("Test Course")
        self.page.select_exam_date("2025-01-01")
        self.page.select_public_filter()
        self.page.enter_participants("1")
        self.page.select_order_by("Newest")
        self.page.click_apply_filters()

    def test_clear_filters(self) -> None:
        """Test clearing all applied filters and returning to the full list of groups."""
        self.page.toggle_filters()
        self.page.enter_course("Test Course")
        self.page.select_private_filter()
        self.page.click_clear_filters()

    def test_no_matching_results(self) -> None:
        """Test applying filters that return no matching results."""
        self.page.toggle_filters()
        self.page.enter_course("NonExistentCourse")
        self.page.click_apply_filters()
        assert (
            self.page.is_no_results_message_displayed()
        ), "No matching results message not displayed."
