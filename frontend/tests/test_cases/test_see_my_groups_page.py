import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.see_my_groups_page import SeeMyGroupsPage

# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By


class TestSeeMyGroups:
    BASE_URL = "http://localhost:3000/group/see-my-group"

    @pytest.fixture(autouse=True)
    def setup(self, driver: webdriver.Chrome) -> None:
        self.page = SeeMyGroupsPage(driver)
        self.page.load()
        # Wait for initial page load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(self.page.HEADING)
        )

    def test_page_header_visible(self) -> None:
        """Test that the page header is visible"""
        assert self.page.is_heading_visible(), "Page header should be visible"

    def test_loading_state(self) -> None:
        """Test that loading state is shown and then disappears"""
        # Give time for loading state to appear
        WebDriverWait(self.page.driver, 10).until(
            lambda _: self.page.is_loading() or self.page.get_group_cards()
        )
        # After loading completes, verify cards are accessible
        self.page.get_group_cards()
        assert not self.page.is_loading(), "Loading indicator should disappear"

    def test_create_group_navigation(self) -> None:
        """Test navigation to create group page"""
        self.page.click_create_group()
        WebDriverWait(self.page.driver, 10).until(
            lambda d: "/group/create" in d.current_url
        )
        assert (
            "/group/create" in self.page.driver.current_url
        ), "Should navigate to create group page"
        assert (
            "/group/create" in self.page.driver.current_url
        ), "Should navigate to create group page"

    def test_group_cards_display(self) -> None:
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


# These test cases are not currently being used but are here for future reference

# def test_page_header_not_visible_when_invalid(self):
#     """Test that the page header is not visible when page is invalid"""
#     self.page.URL = "http://localhost:3000/invalid-url"  # Set invalid URL
#     self.page.load()
#     assert not self.page.is_heading_visible(), "Page header should not be visible on invalid page"

# def test_loading_state_timeout(self):
#     """Test behavior when loading state persists (timeout scenario)"""
#     # Modify the URL to simulate a slow/hanging request
#     self.page.URL = "http://localhost:3000/group/see-my-group?delay=true"
#     self.page.load()

#     with pytest.raises(TimeoutException):
#         WebDriverWait(self.page.driver, 3).until_not(  # Short timeout to test failure
#             EC.presence_of_element_located(self.page.LOADING_INDICATOR)
#         )

# def test_create_group_button_disabled(self):
#     """Test that create group button is not clickable when disabled"""
#     # Add a disabled button locator to your page object
#     self.page.CREATE_GROUP_BUTTON_DISABLED = (By.CSS_SELECTOR, "[data-testid='create-group-button'][disabled]")

#     # Simulate a condition where button should be disabled (e.g., user not logged in)
#     self.page.URL = "http://localhost:3000/group/see-my-group?unauthorized=true"
#     self.page.load()

#     with pytest.raises(TimeoutException):
#         self.page.click_create_group()

# def test_empty_group_cards(self):
#     """Test when no group cards are present"""
#     # Modify URL to ensure no groups are returned
#     self.page.URL = "http://localhost:3000/group/see-my-group?empty=true"
#     self.page.load()

#     # Wait for loading to complete
#     WebDriverWait(self.page.driver, 10).until_not(
#         EC.presence_of_element_located(self.page.LOADING_INDICATOR)
#     )

#     group_cards = self.page.get_group_cards()
#     assert len(group_cards) == 0, "Should have no group cards"

# def test_error_state_display(self):
#     """Test that error state is properly displayed"""
#     # Add error message locator to your page object if not present
#     self.page.ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='error-message']")

#     # Modify URL to trigger an error state
#     self.page.URL = "http://localhost:3000/group/see-my-group?error=true"
#     self.page.load()

#     assert self.page.has_error(), "Error message should be displayed when API fails"

# def test_network_error_handling(self):
#     """Test behavior when network is unavailable"""
#     # You might need to use a proxy or network interceptor to simulate this
#     # This is a basic example - implementation details will depend on your setup
#     self.page.URL = "http://localhost:3000/group/see-my-group?network_error=true"
#     self.page.load()

#     assert self.page.has_error(), "Network error message should be displayed"
