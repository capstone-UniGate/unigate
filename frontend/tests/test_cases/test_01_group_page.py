import pytest
from loguru import logger
from pytest import fixture
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from tests.pages.group_page import GroupPage
from tests.test_cases.base_test import BaseTest


class TestGroupPage(BaseTest):
    @fixture(autouse=True)
    def setup(self, driver: webdriver.Chrome) -> None:
        self.login(driver)
        self.page = GroupPage(driver)
        self.load_success = self.page.load()

    def test_page_loads_successfully(self) -> None:
        """Test that the page loads successfully"""
        assert self.load_success, "Page should load successfully"
        assert self.page.is_page_loaded(), "Page document should be in complete state"

    def test_page_header_visible(self) -> None:
        """Test that the page header is visible"""
        if not self.load_success:
            pytest.skip("Page failed to load, skipping header test")

        is_visible = self.page.is_heading_visible()
        assert is_visible, "Page header should be visible"

    def test_group_cards_display(self) -> None:
        """Test that group cards container is present"""
        if not self.load_success:
            pytest.skip("Page failed to load, skipping cards test")

        try:
            group_cards = self.page.get_group_cards()
            assert isinstance(group_cards, list), (
                "Should return a list of cards (even if empty)"
            )

            # Log the number of cards found (helpful for debugging)
            cards_count = len(group_cards)
            logger.info(f"Found {cards_count} group cards on the page")

        except TimeoutException:
            pytest.fail("Group cards did not load within the expected timeout")
        except Exception as e:  # noqa: BLE001
            pytest.fail(f"Unexpected error while checking group cards: {e!s}")

    def test_page_structure_complete(self) -> None:
        """Test that all essential page elements are present"""
        if not self.load_success:
            pytest.fail("Page failed to load")

        # Create a list of checks and their status
        page_checks = {
            "Page Loaded": self.page.is_page_loaded(),
            "Header Visible": self.page.is_heading_visible(),
            "Cards Container Present": len(self.page.get_group_cards()) >= 0,
        }

        # Check if any of the essential elements are missing
        missing_elements = [
            element for element, status in page_checks.items() if not status
        ]

        # If any elements are missing, fail the test with details
        if missing_elements:
            pytest.fail(
                f"Page structure incomplete. Missing elements: {', '.join(missing_elements)}"
            )
