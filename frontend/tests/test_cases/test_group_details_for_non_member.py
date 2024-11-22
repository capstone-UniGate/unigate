from selenium.webdriver.common.by import By

from tests.pages.group_page_detail import GroupPageDetail


def test_group_details_for_non_member(driver):
    """Test that a non-member student sees the correct details on a private group page."""

    # Arrange: Set up the group details
    group_id = "4"  # Use a private group's ID for testing
    group_page = GroupPageDetail(driver, group_id=group_id)

    # Act: Load the group details page
    group_page.load()

    # Assert: Verify the group description is displayed
    description_element = driver.find_element(By.CSS_SELECTOR, ".text-gray-600")
    assert description_element.is_displayed(), "Group description is not displayed."
    assert description_element.text != "", "Group description is empty."

    # Assert: Verify the link to view members
    members_link = driver.find_element(By.CSS_SELECTOR, "a.text-blue-500")
    assert members_link.is_displayed(), "Link to view members is not displayed."
    assert "/group/" in members_link.get_attribute(
        "href"
    ), "Members link URL is incorrect."

    # Assert: Verify the "Join" button is visible
    join_button = driver.find_element(
        By.XPATH, "//button[contains(text(), 'Join Group')]"
    )
    assert join_button.is_displayed(), "Join button is not displayed for non-members."

    print("Test passed: Group details are displayed correctly for a non-member.")
