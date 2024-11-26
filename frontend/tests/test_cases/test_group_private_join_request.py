import pytest
from pytest import fixture
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from tests.pages.request_page import RequestPage


class TestGroupPageJoinRequests:
    @fixture(autouse=True)
    def setup(self, driver: webdriver.Chrome) -> None:
        self.page = RequestPage(driver)
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

    # def test_requests_list_display(self) -> None:
    #     """Test that group cards container is present"""
    #     if not self.load_success:
    #         pytest.skip("Page failed to load, skipping cards test")

    #     try:
    #         requests_list = self.page.get_requests_list()
    #         assert isinstance(
    #             requests_list, list
    #         ), "Should return a list of cards (even if empty)"

    #         # Log the number of cards found (helpful for debugging)
    #         cards_count = len(requests_list)
    #         logger.info(f"Found {cards_count} group cards on the page")

    #     except TimeoutException:
    #         pytest.fail("Group cards did not load within the expected timeout")
    #     except Exception as e:
    #         pytest.fail(f"Unexpected error while checking group cards: {e!s}")

    def test_click_approve(self) -> None:
        """Test clicking the approve button"""
        if not self.load_success:
            pytest.skip("Page failed to load, skipping approve button test")

        try:
            self.page.click_approve(self.page.select_request())
        except TimeoutException:
            pytest.fail("Approve button did not load within the expected timeout")
        except Exception as e:  # noqa: BLE001
            pytest.fail(f"Unexpected error while clicking approve button: {e!s}")

    def test_click_reject(self) -> None:
        """Test clicking the reject button"""
        if not self.load_success:
            pytest.skip("Page failed to load, skipping reject button test")

        try:
            self.page.click_reject(self.page.select_request())
        except TimeoutException:
            pytest.fail("Reject button did not load within the expected timeout")
        except Exception as e:  # noqa: BLE001
            pytest.fail(f"Unexpected error while clicking reject button: {e!s}")
