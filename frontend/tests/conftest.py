from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from .constants import Urls  # Import BASE_URL from constants


@pytest.fixture(scope="session")
def driver() -> Generator[webdriver.Chrome, None, None]:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    service = Service()
    driver = webdriver.Chrome(options=chrome_options, service=service)
    driver.implicitly_wait(10)
    # Navigate to base URL
    driver.get(Urls.BASE_URL)
    yield driver
    driver.quit()
