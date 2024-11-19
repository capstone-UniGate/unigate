from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from tests.pages.my_groups_page import MyGroupsPage
from tests.utils import wait_until_ec


def test_see_my_groups(driver: webdriver.Chrome) -> None:
    my_groups_page = MyGroupsPage(driver)
    my_groups_page.load()

    # wait for groups cars
    wait_until_ec(driver, presence_of_element_located, (By.CLASS_NAME, "bg-card"))
    groups = driver.find_elements(By.CLASS_NAME, "bg-card")
    assert len(groups) == 10
