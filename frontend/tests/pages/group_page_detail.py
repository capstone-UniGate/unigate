from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait


class GroupPageDetail:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 1000)

    def is_manage_requests_section_visible(self) -> bool:
        """Check if the Manage Join Requests section is visible."""
        try:
            section = self.driver.find_element(By.CLASS_NAME, "scroll-area")
            return section.is_displayed()
        except Exception:  # noqa: BLE001
            return False

    def get_join_requests(self) -> list[WebElement] | None:
        """Return all join requests as elements."""
        return self.driver.find_elements(By.CSS_SELECTOR, ".scroll-area ul li")

    def approve_request(self, request_index: int) -> None:
        """Approve a join request by its index."""
        requests = self.get_join_requests()
        if requests is None:
            raise TypeError
        if request_index >= len(requests):
            raise IndexError("Request index out of range.")
        approve_button = requests[request_index].find_element(
            By.XPATH, ".//button[contains(@alt, 'Approved')]"
        )
        approve_button.click()

    def reject_request(self, request_index: int) -> None:
        """Reject a join request by its index."""
        requests = self.get_join_requests()
        if requests is None:
            raise TypeError
        if request_index >= len(requests):
            raise IndexError("Request index out of range.")
        reject_button = requests[request_index].find_element(
            By.XPATH, ".//button[contains(@alt, 'Reject')]"
        )
        reject_button.click()

    def block_request(self, request_index: int) -> None:
        """Block a join request by its index."""
        requests = self.get_join_requests()
        if requests is None:
            raise TypeError
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
        return (self.get_toast()).text

    def get_toast(self) -> WebElement:
        return self.driver.find_element(
            By.CSS_SELECTOR, '[data-state="open"][data-swipe-direction="right"]'
        )

    def toast_disappearence(self) -> None:
        self.wait.until(EC.none_of(EC.visibility_of(self.get_toast())))

    def click_join(self) -> None:
        create_button = self.driver.find_element(By.ID, "join-group-button")
        # create_button.send_keys(Keys.ENTER)
        create_button.click()

    def click_leave(self) -> None:
        leave_button = self.driver.find_element(By.ID, "leave-group-button")
        # leave_button.send_keys(Keys.ENTER)
        leave_button.click()

    def click_members(self) -> None:
        members_button = self.driver.find_element(By.ID, "members_list")
        # members_button.send_keys(Keys.ENTER)
        members_button.click()

    def check_description(self) -> bool:
        description_element = self.driver.find_element(
            By.CSS_SELECTOR, ".text-gray-600"
        )
        return description_element.is_displayed() and description_element.text != ""

    def check_members_link(self) -> bool:
        members_link = self.driver.find_element(By.CSS_SELECTOR, "a.text-blue-500")
        return members_link.is_displayed()

    def check_ask_join(self) -> bool:
        join_button = self.driver.find_element(By.ID, "ask-to-join-button")
        return join_button.is_displayed()

    def check_leave(self) -> bool:
        leave_button = self.driver.find_element(By.ID, "leave-group-button")
        return leave_button.is_displayed()

    def check_manage(self) -> bool:
        manage_button = self.driver.find_element(By.ID, "Manage_requests")
        return manage_button.is_displayed()
