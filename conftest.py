import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import BASE_URL, LOGIN_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from pages.login_page import LoginPage

HEADLESS = os.environ.get("HEADLESS", "true").lower() != "false"
BROWSER = os.environ.get("BROWSER", "chrome").lower()

SIDEBAR_ITEM = (By.CSS_SELECTOR, ".oxd-main-menu-item--name")
LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, ".oxd-select-text")
SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")


def _is_english(driver):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    WebDriverWait(driver, 15).until(EC.presence_of_element_located(SIDEBAR_ITEM))
    labels = [s.text for s in driver.find_elements(*SIDEBAR_ITEM) if s.text]
    return "Admin" in labels


def _reset_system_language_to_english(driver):
    # This demo account is shared by everyone practicing Selenium against it.
    # Anyone can change the global default language via Admin > Configuration >
    # Localization, which silently breaks every English-text locator for
    # everyone else's session too. Detect it and self-heal rather than fail.
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(driver, 15)
    driver.get(f"{BASE_URL}/admin/localization")
    wait.until(EC.presence_of_element_located(LANGUAGE_DROPDOWN)).click()
    option_locator = (By.XPATH, "//div[@role='listbox']//span[contains(.,'English')]")
    wait.until(EC.element_to_be_clickable(option_locator)).click()
    wait.until(EC.element_to_be_clickable(SAVE_BUTTON)).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-toast")))


def _build_chrome_driver():
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-background-timer-throttling")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def _build_firefox_driver():
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from webdriver_manager.firefox import GeckoDriverManager

    options = Options()
    if HEADLESS:
        options.add_argument("-headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)


@pytest.fixture
def driver():
    if BROWSER == "firefox":
        drv = _build_firefox_driver()
    else:
        drv = _build_chrome_driver()
    if not HEADLESS:
        drv.maximize_window()
    yield drv
    drv.quit()


@pytest.fixture
def logged_in_driver(driver):
    driver.get(LOGIN_URL)
    LoginPage(driver).login(ADMIN_USERNAME, ADMIN_PASSWORD)

    if not _is_english(driver):
        _reset_system_language_to_english(driver)
        driver.get(LOGIN_URL)
        LoginPage(driver).login(ADMIN_USERNAME, ADMIN_PASSWORD)

    return driver
