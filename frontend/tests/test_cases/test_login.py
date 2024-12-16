import time

import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec

from tests.constants import TestData, Urls
from tests.pages.login_page import LoginPage
from tests.test_cases.base_test import BaseTest


class TestLogin(BaseTest):
    @pytest.fixture
    def page(self, base_page: webdriver.Chrome) -> LoginPage:
        page = LoginPage(base_page)
        page.navigate()
        return page

    def test_successful_login(self, page: LoginPage) -> None:
        # Fill in the form with valid credentials
        page.enter_username(TestData.VALID_USERNAME)

        page.enter_password(TestData.VALID_PASSWORD)
        page.click_login()

        # Wait for successful redirection to dashboard
        self.wait.until(ec.url_to_be(url=Urls.GROUP_PAGE))

        # Assert that the user is successfully logged in
        assert "Welcome" in page.get_success_message()

    def test_failed_login_invalid_credentials(self, page: LoginPage) -> None:
        # Define expected error message for invalid login
        time.sleep(1)
        expected_error_msg = "Login failed."

        # Enter invalid credentials and attempt to log in
        page.enter_username(TestData.INVALID_USERNAME)
        page.enter_password(TestData.INVALID_PASSWORD)
        page.click_login()

        # Wait for the error message to appear
        error_message = page.get_error_message()

        # Assert that the correct error message is displayed
        assert (
            error_message == expected_error_msg
        ), f"Expected '{expected_error_msg}', but got '{error_message}'"
        time.sleep(1)

        # Ensure the username and password fields are cleared for re-entry
        assert page.is_username_empty()
        assert page.is_password_empty()

    def test_login_network_error(self, page: LoginPage) -> None:
        time.sleep(1)

        page.enter_username(TestData.VALID_USERNAME)
        page.enter_password(TestData.VALID_PASSWORD)
        page.click_login()

        # Simulate network error
        page.simulate_network_error()

        assert page.is_login_page()

        # Restore the network
        page.restore_network()

    # def test_redirect_to_login_on_restricted_access(self, page: LoginPage) -> None:
    #     page.navigate_to_restricted_page()

    #     # Assert that the user is redirected to the login page
    #     self.wait.until(EC.url_to_be(url=Urls.LOGIN_PAGE))

    #     # Check for the redirect message
    #     # assert "Please log in to access this feature." in page.get_success_message()
    #     assert page.is_login_page()
