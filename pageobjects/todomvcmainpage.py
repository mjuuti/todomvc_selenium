"""
Minimal page object module for TODOMVC.com main page
"""
from page_objects import PageElement
from pageobjects.basepage import BasePage


class TodoMvcMainPage(BasePage):
    """Page object for the main page"""

    emberjs_link = PageElement(css='a[data-source="http://emberjs.com"]')

    def __init__(self):
        self.url = 'http://todomvc.com'
        self.path = '/'
        super().__init__(self.url)
        self.required_element = ['emberjs_link']
