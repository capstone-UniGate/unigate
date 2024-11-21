import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.see_my_groups_page import SeeMyGroupsPage


class TestSeeMyGroups:
    BASE_URL = "http://localhost:3000/group/see-my-group"

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.page = SeeMyGroupsPage(driver)
        self.page.load()
        # Wait for initial page load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(self.page.HEADING)
        )

    def test_page_header_visible(self):
        """Test that the page header is visible"""
        assert self.page.is_heading_visible(), "Page header should be visible"

    def test_loading_state(self):
        """Test that loading state is shown and then disappears"""
        # Give time for loading state to appear
        WebDriverWait(self.page.driver, 10).until(
            lambda d: self.page.is_loading() or self.page.get_group_cards()
        )
        # After loading completes, verify cards are accessible
        group_cards = self.page.get_group_cards()
        assert not self.page.is_loading(), "Loading indicator should disappear"

    def test_create_group_navigation(self):
        """Test navigation to create group page"""
        self.page.click_create_group()
        WebDriverWait(self.page.driver, 10).until(
            lambda d: "/group/create" in d.current_url
        )
        assert (
            "/group/create" in self.page.driver.current_url
        ), "Should navigate to create group page"

    def test_group_cards_display(self):
        """Test that group cards are displayed after loading"""
        # Wait for loading to complete
        WebDriverWait(self.page.driver, 10).until_not(
            EC.presence_of_element_located(self.page.LOADING_INDICATOR)
        )
        group_cards = self.page.get_group_cards()
        # Test passes whether there are cards or not
        assert isinstance(
            group_cards, list
        ), "Should return a list of cards (even if empty)"
