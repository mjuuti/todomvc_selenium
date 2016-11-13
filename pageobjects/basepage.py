"""
Base page object module file
"""
from page_objects import PageObject
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from waiting import TimeoutExpired
from waiting import wait
from lib import config


class BasePage(PageObject):
    """Base page object for common methods and WEBDRIVER_CLASS operations"""

    path = '/'
    required_elements = []
    __driver = None

    def __init__(self, base_url):
        super().__init__(self._driver, base_url)

    @property
    def _driver(self) -> WebDriver:
        if not self.__driver:
            self.__driver = config.WEBDRIVER_CLASS()
        return self.__driver

    def open(self, wait_for_loading: bool = True) -> None:
        """
        Open page

        :param bool wait_for_loading: if True wait all required elements on page are found
        :return: None
        """
        self.get(self.path)
        if wait_for_loading:
            self.wait_page_to_load()

    def wait_page_to_load(self, timeout: int = config.TIMEOUT_DEFAULT):
        """
        Wait for page to load

        :param timeout:
        :return:
        """
        for required_element in self.required_elements:
            message = "%s (%s) to be found" % (required_element, self.__class__.__name__)
            wait(lambda: self.is_present(required_element), timeout_seconds=timeout, waiting_for=message)

    def is_page_loaded(self, timeout: int = config.TIMEOUT_DEFAULT):
        """
        Is page loaded

        :param int timeout: Maximum time to wait for elements to appear
        :return: True if all elements are found within timeout, False otherwise
        """
        try:
            self.wait_page_to_load(timeout=timeout)
            return True
        except TimeoutExpired:
            return False

    def is_present(self, locator_name: str) -> bool:
        """
        Return true if element with given name is found from active page

        :param str locator_name: Element locator name
        :return: True if element is found
        """
        element = getattr(self, locator_name, None)
        return element is not None and element.is_displayed()

    def jsclick(self, element: WebElement) -> None:
        """
        Click on element using JavaScript

        :param WebElement element: Element to click
        :return: None
        """
        self.w.execute_script("$(arguments[0]).click();", element)

    def doubleclick(self, element: WebElement) -> None:
        """
        Double-click on given element

        :param WebElement element: Element to double-click
        :return: None
        """
        action = ActionChains(self.w)
        action.move_to_element(element)
        action.double_click(element).perform()

    def __del__(self):
        if self.__driver:
            self.__driver.close()
