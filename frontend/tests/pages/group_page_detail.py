from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver


class GroupPageDetail:
    URL = "http://localhost:3000/groups/{group_id}"

    def __init__(self, driver: WebDriver, group_id: str) -> None:
        self.driver = driver
        self.group_id = group_id

    def navigate(self) -> None:
        self.driver.get(self.URL)

    def load(self) -> None:
        """Load the group page."""
        self.driver.get(self.URL.format(group_id=self.group_id))

    def is_manage_requests_section_visible(self) -> bool:
        """Check if the Manage Join Requests section is visible."""
        try:
            section = self.driver.find_element(By.CLASS_NAME, "scroll-area")
            return section.is_displayed()
        except Exception:  # noqa: BLE001
            return False

    def get_join_requests(self) -> list | None:
        """Return all join requests as elements."""
        return self.driver.find_elements(By.CSS_SELECTOR, ".scroll-area ul li")

    def approve_request(self, request_index: int) -> None:
        """Approve a join request by its index."""
        requests = self.get_join_requests()
        if request_index >= len(requests):
            raise IndexError("Request index out of range.")
        approve_button = requests[request_index].find_element(
            By.XPATH, ".//button[contains(@alt, 'Approved')]"
        )
        approve_button.click()

    def reject_request(self, request_index: int) -> None:
        """Reject a join request by its index."""
        requests = self.get_join_requests()
        if request_index >= len(requests):
            raise IndexError("Request index out of range.")
        reject_button = requests[request_index].find_element(
            By.XPATH, ".//button[contains(@alt, 'Reject')]"
        )
        reject_button.click()

    def block_request(self, request_index: int) -> None:
        """Block a join request by its index."""
        requests = self.get_join_requests()
        if request_index >= len(requests):
            raise IndexError("Request index out of range.")
        block_button = requests[request_index].find_element(
            By.XPATH, ".//button[contains(@alt, 'Block')]"
        )
        block_button.click()

    def get_toast_message(self) -> str:
        """Retrieve the text from the success toast message."""
        # WebDriverWait(self.driver, 10).until(
        #    ec.visibility_of_element_located((By.CLASS_NAME, "toast-success"))
        # )
        toast_message = self.driver.find_element(
            By.CSS_SELECTOR, '[data-state="open"][data-swipe-direction="right"]'
        )
        return toast_message.text

    def click_join(self) -> None:
        create_button = self.driver.find_element(By.ID, "join-group-button")

        create_button.click()

    def click_leave(self) -> None:
        leave_button = self.driver.find_element(By.ID, "leave-group-button")
        leave_button.send_keys(Keys.ENTER)
        leave_button.click()
