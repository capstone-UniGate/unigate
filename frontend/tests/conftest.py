from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver() -> Generator[webdriver.Chrome, None, None]:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()
