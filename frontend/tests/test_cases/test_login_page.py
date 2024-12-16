import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from tests.pages.login_page import LoginPage
from tests.constants import Urls

@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_login_page(driver: WebDriver):
    login_page = LoginPage(driver)
    login_page.load()
    
    # Wait until the login page is loaded
    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == login_page.URL
    )
    assert driver.current_url == login_page.URL

def test_login_page_elements(driver: WebDriver):
    login_page = LoginPage(driver)
    login_page.load()
    
    # Use the LoginPage class methods to check if elements are displayed
    assert login_page.is_element_displayed(LoginPage.USERNAME_XPATH)
    assert login_page.is_element_displayed(LoginPage.PASSWORD_XPATH)
    assert login_page.is_element_displayed(LoginPage.LOGIN_BUTTON_XPATH)

def test_successful_login(driver: WebDriver):
    login_page = LoginPage(driver)
    login_page.load()
    
    # Input valid credentials and submit
    login_page.enter_username("S1234567")
    login_page.enter_password("testpassword")
    login_page.click_login_button()
    
    # Wait until the user is redirected to the groups page
    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == Urls.GROUP_PAGE  # Use Urls.GROUP_PAGE
    )
    assert driver.current_url == Urls.GROUP_PAGE  # Use Urls.GROUP_PAGE

def test_invalid_login(driver: WebDriver):
    login_page = LoginPage(driver)
    login_page.load()
    
    # Input invalid credentials and submit
    login_page.enter_username("wronguser")
    login_page.enter_password("wrongpassword")
    login_page.click_login_button()
    
    # Wait for the error message
    error_message = login_page.get_error_message()
    
    assert error_message.is_displayed()
    assert error_message.text == "Login failed."

def test_retry_after_failed_login(driver: WebDriver):
    login_page = LoginPage(driver)
    login_page.load()

    # Attempt to log in with incorrect credentials
    login_page.enter_username("wronguser")
    login_page.enter_password("wrongpassword")
    login_page.click_login_button()

    # Wait for the error message after failed login
    error_message = login_page.get_error_message()
    assert error_message.is_displayed()
    assert error_message.text == "Login failed."

    # Retry with correct credentials
    login_page.enter_username("S1234567")
    login_page.enter_password("testpassword")
    login_page.click_login_button()

    # Wait until the user is redirected to the groups page after successful login
    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == Urls.GROUP_PAGE
    )
    assert driver.current_url == Urls.GROUP_PAGE

def test_username_empty_login_button_disabled(driver: WebDriver):
    login_page = LoginPage(driver)
    login_page.load()

    # Leave username empty and enter a valid password
    login_page.enter_username("")  # Empty username
    login_page.enter_password("testpassword")
    
    # Check if the login button is disabled
    assert login_page.is_login_button_disabled()

def test_password_empty_login_button_disabled(driver: WebDriver):
    login_page = LoginPage(driver)
    login_page.load()

    # Leave password empty and enter a valid username
    login_page.enter_username("S1234567")
    login_page.enter_password("")  # Empty password
    
    # Check if the login button is disabled
    assert login_page.is_login_button_disabled()
