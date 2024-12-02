from pytest import fixture
from selenium import webdriver

from tests.pages.group_page_detail import GroupPageDetail


class TestLeaveGroup:
    @fixture(autouse=True)
    def setup(self, driver: webdriver.Chrome) -> None:
        group_id = "1"
        self.page = GroupPageDetail(driver, group_id=group_id)
        self.load_success = self.page.load()

    def test_leave_group(self) -> None:
        self.page.click_leave()
        text = self.page.get_toast_message()
        assert text == "You have left the group"
