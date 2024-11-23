from collections.abc import Callable
from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.expected_conditions import WebDriverOrWebElement
from selenium.webdriver.support.ui import WebDriverWait


def wait_until_ec(
    driver: WebDriver,
    condition_function: Callable[
        [tuple[str, str]], Callable[[WebDriverOrWebElement], WebElement]
    ],
    locators: tuple[str, str] | list[tuple[str, str]],
    duration: float = 10.0,
    frequency: float = 0.5,
    *,
    check_all: bool = False,
) -> WebElement | list[WebElement]:
    """
    Waits until the specified Expected Condition(s) is met.

    Args:
        driver (WebDriver): The WebDriver instance.
        condition_function (Callable[[tuple[str, str]], Callable[[WebDriverOrWebElement], WebElement]]): An Expected Condition function from `selenium.webdriver.support.expected_conditions`.
        locators (tuple[str, str] | list[tuple[str, str]]): A locator tuple (By, locator) or a list of such tuples.
        duration (float, optional): Maximum time to wait in seconds. Defaults to 10.0.
        frequency (float, optional): Polling frequency in seconds. Defaults to 0.5.
        check_all (bool, optional): If True, waits until all conditions are met; otherwise, any one condition. Defaults to False.

    Returns:
        WebElement | list[WebElement]: The result of the wait condition.

    Raises:
        selenium.common.exceptions.TimeoutException: If the condition is not met within the specified duration.
    """

    if isinstance(locators, tuple):
        locators = [locators]
    conditions = [condition_function(locator) for locator in locators]

    combined_condition = EC.all_of(*conditions) if check_all else EC.any_of(*conditions)

    wait = WebDriverWait(driver, duration, frequency)
    return wait.until(combined_condition)


def wait_until(
    driver: WebDriver,
    function: Callable[[WebDriver], Any],
    duration: float = 10.0,
    frequency: float = 0.5,
) -> WebElement | list[WebElement]:
    """
    Waits until a custom condition function returns a truthy value.

    Args:
        driver (WebDriver): The WebDriver instance.
        function (Callable[[WebDriver], Any]): A callable that accepts the driver and returns a truthy value when the condition is met.
        duration (float, optional): Maximum time to wait in seconds. Defaults to 10.0.
        frequency (float, optional): Polling frequency in seconds. Defaults to 0.5.

    Returns:
        WebElement | list[WebElement]: The result returned by the condition function.

    Raises:
        selenium.common.exceptions.TimeoutException: If the condition is not met within the specified duration.
    """

    wait = WebDriverWait(driver, duration, frequency)
    return wait.until(lambda drv: function(drv))
