from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait


class GroupPageDetail:
    # Element Locators
    # BLOCK_BUTTON = (By.CSS_SELECTOR, '[data-test="block-user-button"]')

    REQUESTS_SECTION = (By.XPATH, "//div[@v-if='showRequests']")
    BLOCK_BUTTON_XPATH = (
        By.XPATH,
        "//button[normalize-space(text())='Block']",
    )  # Using text-based XPath

    REQUEST_ITEM = (By.CSS_SELECTOR, ".request-item")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".toast-success")
    ERROR_TOAST = (By.CSS_SELECTOR, ".toast-error")
    LOADING_INDICATOR = (By.CSS_SELECTOR, ".loading-indicator")
    REQUEST_LIST = (By.CSS_SELECTOR, ".requests-list")
    MANAGE_REQUESTS_BUTTON = (By.ID, "Manage_requests")

    BLOCK_BUTTONS = (
        By.XPATH,
        "//button[contains(@class, 'bg-red-500') and text()='Block']",
    )

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

    def click_block_user_button(self):
        block_button = self.wait.until(EC.element_to_be_clickable(self.BLOCK_BUTTON))
        block_button.click()

    def confirm_block_action(self):
        block_button = self.wait.until(EC.element_to_be_clickable(self.BLOCK_BUTTON))
        block_button.click()

    def verify_user_blocked(self):
        toast = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_TOAST))
        assert "User has been successfully blocked from the group." in toast.text

    def verify_request_removed(self, request_id):
        requests = self.driver.find_elements(*self.REQUEST_LIST)
        for request in requests:
            assert request_id not in request.text

    def verify_loading_indicator_visible(self):
        self.wait.until(EC.visibility_of_element_located(self.LOADING_INDICATOR))

    def verify_error_message(self, message):
        toast = self.wait.until(EC.visibility_of_element_located(self.ERROR_TOAST))
        assert message in toast.text

    def click_request_item(self, request_id):
        request_item = self.wait.until(
            EC.element_to_be_clickable(self.MANAGE_REQUESTS_BUTTON)
        )
        request_item.click()

    def click_block_button(self, request_index: int = 0) -> None:
        self.wait.until(EC.presence_of_element_located(self.REQUESTS_SECTION))
        # Wait for the Block button to be clickable based on text (assumes first button found is correct)
        block_button = self.wait.until(
            EC.element_to_be_clickable(self.BLOCK_BUTTON_XPATH)
        )

        # Click the Block button
        block_button.click()
