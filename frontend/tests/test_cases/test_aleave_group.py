from pytest import fixture
from selenium import webdriver

from tests.pages.group_page_detail import GroupPageDetail


class TestLeaveGroup:
    @fixture(autouse=True)
    def setup(self, driver: webdriver.Chrome) -> None:
        self.page = GroupPageDetail(
            driver, group_id="05e6af32-6990-467b-8b03-8557a9b84e56"
        )
        self.page.load()

    def test_leave_group(self) -> None:
        self.page.click_join()
        self.page.toast_disappearence()
        self.page.click_leave()
        text = self.page.get_toast_message()
        assert text == "You have left the group"
