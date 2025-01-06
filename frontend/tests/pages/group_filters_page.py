from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select


class GroupFiltersPage:
    # XPath Selectors
    SELECTORS = {
        "filter_toggle_button": '//div[@id="__nuxt"]/div/div/main/div/div/div/button/span',
        "apply_filters_button": '//div[@id="__nuxt"]/div/div/main/div/div/div[2]/div[2]/button',
        "clear_filters_button": '//div[@id="__nuxt"]/div/div/main/div/div/div[2]/div[2]/button[2]',
        "course_search_box": '//div[@id="course"]/input',
        "exam_date_dropdown": '//div[@id="__nuxt"]/div/div/main/div/div/div[2]/div/div[2]/div/select',
        "participants_input": '//input[@id="participants"]',
        "is_public_dropdown": '//div[@id="__nuxt"]/div/div/main/div/div/div[2]/div/div[4]/select',
        "order_by_dropdown": '//div[@id="__nuxt"]/div/div/main/div/div/div[2]/div/div[5]/select',
        "no_results_message": '//div[@class="mt-4 p-4 bg-red-100 text-red-700 rounded-lg"]',
    }

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def load(self):
        self.driver.get("/groups")

    # Helper function to click an element
    def click_element(self, selector: str):
        self.driver.find_element(By.XPATH, selector).click()

    # Helper function to enter text into an input field
    def enter_text(self, selector: str, text: str):
        element = self.driver.find_element(By.XPATH, selector)
        element.clear()
        element.send_keys(text)

    # Helper function to select a dropdown option
    def select_option(self, selector: str, value: str):
        dropdown = Select(self.driver.find_element(By.XPATH, selector))
        dropdown.select_by_visible_text(value)

    # Actions using helper functions
    def toggle_filters(self):
        self.click_element(self.SELECTORS["filter_toggle_button"])

    def click_apply_filters(self):
        self.click_element(self.SELECTORS["apply_filters_button"])

    def click_clear_filters(self):
        self.click_element(self.SELECTORS["clear_filters_button"])

    def enter_course(self, course_name: str):
        self.enter_text(self.SELECTORS["course_search_box"], course_name)

    def select_exam_date(self, date: str):
        self.select_option(self.SELECTORS["exam_date_dropdown"], date)

    def enter_participants(self, number: str):
        self.enter_text(self.SELECTORS["participants_input"], number)

    def select_public_filter(self):
        self.select_option(self.SELECTORS["is_public_dropdown"], "Public")

    def select_private_filter(self):
        self.select_option(self.SELECTORS["is_public_dropdown"], "Private")

    def select_order_by(self, order: str):
        self.select_option(self.SELECTORS["order_by_dropdown"], order)

    def is_no_results_message_displayed(self) -> bool:
        elements = self.driver.find_elements(
            By.XPATH, self.SELECTORS["no_results_message"]
        )
        return len(elements) > 0
