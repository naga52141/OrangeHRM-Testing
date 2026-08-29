import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import LOGIN_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from pages.login_page import LoginPage

HEADLESS = os.environ.get("HEADLESS", "true").lower() != "false"


@pytest.fixture
def driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-background-timer-throttling")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    if not HEADLESS:
        drv.maximize_window()
    yield drv
    drv.quit()


@pytest.fixture
def logged_in_driver(driver):
    driver.get(LOGIN_URL)
    LoginPage(driver).login(ADMIN_USERNAME, ADMIN_PASSWORD)
    return driver
