import time

import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls
from tests.pages.login_page import LoginPage
from tests.pages.main_page import MainPage
from tests.test_cases.base_test import BaseTest


class TestLogout(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, driver: webdriver.Chrome) -> None:
        self.login(driver)
        self.main_page = MainPage(driver)
        self.login_page = LoginPage(driver)
        # Start from main page (already logged in)
        self.main_page.load()
        # Wait for initial page load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(self.main_page.LOGOUT_BUTTON)
        )

    def test_successful_logout(self) -> None:
        """
        Test that verifies the logout functionality:
        1. Starting from main page (already logged in)
        2. Click logout button
        3. Verify redirect to login page
        4. Verify login form is visible
        """
        # Perform logout
        self.main_page.click_logout()

        # Wait for login form to be visible
        WebDriverWait(self.main_page.driver, 10).until(
            EC.visibility_of_element_located(self.login_page.LOGIN_FORM)
        )
        time.sleep(1)

        # Verify redirected to login page
        assert (
            self.login_page.is_login_form_visible()
        ), "Login form should be visible after logout"
        # print(f"{Urls.BASE_URL}/login?message=You+have+successfully+logged+out.")
        assert (
            self.login_page.driver.current_url
            == f"{Urls.BASE_URL}/login?message=You%20have%20successfully%20logged%20out."
        ), "Should be redirected to login page"
