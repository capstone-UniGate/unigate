from .base_page import BasePage


class MyGroupsPage(BasePage):
    URL = "http://localhost:3000/group/see-my-group"

    def load(self) -> None:
        self.driver.get(self.URL)
