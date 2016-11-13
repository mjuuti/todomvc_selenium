"""
Configuration module
"""
import os
from selenium.webdriver import Chrome, Firefox

TIMEOUT_DEFAULT = 10
WEBDRIVER_BROWSER = os.getenv('WEBDRIVER_BROWSER', 'chrome')

_driver_map = {
    'chrome': Chrome,
    'firefox': Firefox
}
WEBDRIVER_CLASS = _driver_map[WEBDRIVER_BROWSER.lower()]
