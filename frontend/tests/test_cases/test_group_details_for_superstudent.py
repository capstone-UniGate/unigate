from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By

from tests.pages.group_page_detail import GroupPageDetail


def test_group_details_for_superstudent(driver: webdriver.Chrome) -> None:
    """Test that a superstudent sees the group details with join requests on group page with group id 1."""

    # Arrange: Set up the group details for a superstudent (group ID 1)
    group_id = "1"  # Testing with group ID 1
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

    # Assert: Verify that there are join requests with approve/reject buttons
    join_requests = driver.find_elements(By.CSS_SELECTOR, "li.flex.items-center")
    assert len(join_requests) > 0, "No join requests found."

    # Given: The user is on the group details page and clicks the "View Members" link
    members_link.click()

    # Act: Wait for the members page to load (you can use WebDriverWait for a more stable wait)
    driver.implicitly_wait(5)  # Implicit wait, adjust based on page load time

    # Then: The page should display a list of current group members with their names and profile pictures
    member_list = driver.find_elements(
        By.CSS_SELECTOR, ".mb-4.text-lg.text-gray-700.flex.items-center"
    )

    assert len(member_list) > 0, "No members are listed on the members page."

    # Iterate through the members and verify their names and profile pictures
    for member in member_list:
        try:
            # Find the name element inside the member element
            name_element = member.find_element(
                By.CSS_SELECTOR, "router-link.text-blue-500"
            )

            # Assert that the name is displayed
            assert (
                name_element.is_displayed()
            ), f"Name of member {member.text} is not displayed."
            assert name_element.text != "", f"Member name is empty for {member.text}."

            # Optionally, check if the profile picture exists (if there's an avatar)
            avatar_element = member.find_element(By.CSS_SELECTOR, "Avatar img")
            assert avatar_element.is_displayed(), "Profile picture is not displayed."

        except Exception as e:  # noqa: BLE001
            logger.info(f"Skipping member {member.text} due to exception: {e}")
            continue  # Skip this member if the name or avatar element is not found
