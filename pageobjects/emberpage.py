"""
Page object definition module for EmberJS page on TODOMVC.com

@author: Markus Juuti
"""
from page_objects import PageElement, MultiPageElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from pageobjects.todomvcmainpage import TodoMvcMainPage


class EmberJsPage(TodoMvcMainPage):
    """Page object for EberJS TODO MVC page"""

    new_todo_entry = PageElement(id_='new-todo')
    todo_entries_visible = MultiPageElement(css='li.ember-view')
    todo_entries_active = MultiPageElement(css='li.ember-view:not([class*="completed"])')
    todo_entries_completed = MultiPageElement(css='li.ember-view.completed')
    toggle_all = PageElement(id_='toggle-all')
    clear_completed = PageElement(id_='clear-completed')
    todo_entry_editing = PageElement(css='input.edit')

    show_all = PageElement(xpath='//a[@class="ember-view" and text()="All"]')
    show_active = PageElement(xpath='//a[@class="ember-view" and text()="Active"]')
    show_completed = PageElement(xpath='//a[@class="ember-view" and text()="Completed"]')

    text_loc = (By.CSS_SELECTOR, 'label')
    close_icon_loc = (By.CSS_SELECTOR, 'button.destroy')
    checkbox_loc = (By.CSS_SELECTOR, 'input.toggle')

    def __init__(self):
        super().__init__()
        self.path += 'examples/emberjs/index.html'
        self.required_elements = ['new_todo_entry']

    def add_new_todo_item(self, todo_text: str) -> None:
        """
        Create new TODO entry

        :param str todo_text: Text to enter
        :return: None
        """
        self.new_todo_entry = todo_text + Keys.ENTER

    def toggle_active(self, element: WebElement) -> None:
        """
        Toggle active state of TODO entry

        :param WebElement element: TODO container element to complete/activate
        :return: None
        """
        checkbox = element.find_element(*self.checkbox_loc)
        checkbox.click()

    def close_todo(self, element: WebElement) -> None:
        """
        Close TODO entry by clicking X

        :param WebElement element: TODO container Element to close
        :return: None
        """
        close_icon = element.find_element(*self.close_icon_loc)
        self.jsclick(close_icon)

    @staticmethod
    def is_todo_active(element: WebElement) -> bool:
        """
        Return True if TODO is active, False otherwise

        :param WebElement element: TODO container element to inspect for completion state
        :return: True if element is not completed
        """
        return 'completed' not in element.get_attribute('class')

    def foo_text(self, element: WebElement) -> str:
        """
        Get text value of TODO element

        :param WebElement element: TODO container Element to get text from
        :return: element text
        """
        text = element.find_element(*self.text_loc)
        return text.text

    def find_todo_by_text(self, text: str) -> WebElement:
        """
        Find TODO container element by visible text

        :param str text: Text to search
        :return: First TODO container element matching search text
        :raises NoSuchElementException if no matching element is found
        """
        for todo in self.todo_entries_visible:
            if todo.text == text:
                return todo
        raise NoSuchElementException("No TODO element found with text '%s'" % text)

    def edit_todo(self, element: WebElement, new_text: str, clear_existing: bool=False):
        """
        Edit existing TODO entry

        :param WebElement element: TODO container element which is edited
        :param str new_text: New todo text
        :param bool clear_existing: Clear field content before sending text if True
        :return: None
        """
        self.doubleclick(element)
        if clear_existing:
            self.todo_entry_editing.clear()
        self.todo_entry_editing = new_text + Keys.ENTER
