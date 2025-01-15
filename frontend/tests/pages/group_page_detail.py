import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait


class GroupPageDetail:
    # Element Locators

    REQUESTS_SECTION = (By.XPATH, "//div[@v-if='showRequests']")

    REQUEST_ITEM = (By.CSS_SELECTOR, ".request-item")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".toast-success")
    ERROR_TOAST = (By.CSS_SELECTOR, ".toast-error")
    LOADING_INDICATOR = (By.CSS_SELECTOR, ".loading-indicator")
    REQUEST_LIST = (By.CSS_SELECTOR, ".requests-list")
    MANAGE_REQUESTS_BUTTON = (By.ID, "Manage_requests")

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
        return self.driver.find_elements(By.ID, "request")

    def get_status(self, request_index: int) -> str:
        """Approve a join request by its index."""
        requests = self.get_join_requests()
        if requests is None:
            raise TypeError
        if request_index >= len(requests):
            raise IndexError("Request index out of range.")
        return requests[request_index].find_element(By.ID, "request_status").text

    def approve_request(self, request_index: int) -> None:
        """Approve a join request by its index."""
        requests = self.get_join_requests()
        if requests is None:
            raise TypeError
        if request_index >= len(requests):
            raise IndexError("Request index out of range.")
        approve_button = requests[request_index].find_element(By.ID, "approve_button")
        approve_button.click()

    def reject_request(self, request_index: int) -> None:
        """Reject a join request by its index."""
        requests = self.get_join_requests()
        if requests is None:
            raise TypeError
        if request_index >= len(requests):
            raise IndexError("Request index out of range.")
        reject_button = requests[request_index].find_element(By.ID, "reject_button")
        reject_button.click()

    def block_request(self, request_index: int) -> None:
        """Block a join request by its index."""
        requests = self.get_join_requests()
        if requests is None:
            raise TypeError
        if request_index >= len(requests):
            raise IndexError("Request index out of range.")
        block_button = requests[request_index].find_element(By.ID, "block_button")
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
        create_button.click()

    def click_ask_to_join(self) -> None:
        create_button = self.driver.find_element(By.ID, "ask-to-join-button")
        time.sleep(0.5)
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
            By.XPATH, "//p[normalize-space()='This is a test group']"
        )
        return description_element.is_displayed() and description_element.text != ""

    def check_members_link(self) -> bool:
        members_link = self.driver.find_element(By.XPATH, "//a[@id='members_list']")
        return members_link.is_displayed()

    def check_ask_join(self) -> bool:
        join_button = self.driver.find_element(By.ID, "ask-to-join-button")
        return join_button.is_displayed()

    def check_join(self) -> bool:
        join_button = self.driver.find_element(By.ID, "join-group-button")
        return join_button.is_displayed()

    def check_leave(self) -> bool:
        leave_button = self.driver.find_element(By.ID, "leave-group-button")
        return leave_button.is_displayed()

    def check_manage(self) -> bool:
        manage_button = self.driver.find_element(By.ID, "Manage_requests")
        return manage_button.is_displayed()

    def click_block_user_button(self) -> None:
        block_button = self.wait.until(EC.element_to_be_clickable(self.BLOCK_BUTTON))
        block_button.click()

    def confirm_block_action(self) -> None:
        block_button = self.wait.until(EC.element_to_be_clickable(self.BLOCK_BUTTON))
        block_button.click()

    def verify_user_blocked(self) -> None:
        toast = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_TOAST))
        assert "User has been successfully blocked from the group." in toast.text

    def verify_request_removed(self, request_id: int) -> None:
        requests = self.driver.find_elements(*self.REQUEST_LIST)
        for request in requests:
            assert request_id not in request.text

    def verify_loading_indicator_visible(self) -> None:
        self.wait.until(EC.visibility_of_element_located(self.LOADING_INDICATOR))

    def verify_error_message(self, message: str) -> None:
        toast = self.wait.until(EC.visibility_of_element_located(self.ERROR_TOAST))
        assert message in toast.text

    def click_request_item(self) -> None:
        request_item = self.wait.until(
            EC.element_to_be_clickable(self.MANAGE_REQUESTS_BUTTON)
        )
        request_item.click()

    def click_block_button(self, request_id: int) -> None:
        # Dynamically generate the selector
        dynamic_selector = (
            f".bg-white:nth-child({request_id}) .inline-flex:nth-child(3)"
        )
        block_button_selector = (By.CSS_SELECTOR, dynamic_selector)

        # Wait for the button to be clickable
        block_button = self.wait.until(
            EC.element_to_be_clickable(block_button_selector)
        )

        # Click the button
        block_button.click()

    def check_req(self) -> bool:
        request_status = self.driver.find_element(By.ID, "request_status_student")
        return (
            request_status.is_displayed()
            and request_status.text == "Your request status: PENDING"
        )

    def click_manage(self) -> None:
        self.driver.find_element(By.ID, "Manage_requests").click()

    def check_no_reqs(self) -> bool:
        return self.driver.find_element(By.ID, "no_requests").is_displayed()

    def click_undo_request(self) -> None:
        undo_button = self.driver.find_element(By.ID, "undo-request-button")
        undo_button.click()
