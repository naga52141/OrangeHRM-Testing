from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage

DASHBOARD_URL = f"{BASE_URL}/dashboard/index"
DIRECTORY_URL = f"{BASE_URL}/directory/viewDirectory"
BUZZ_URL = f"{BASE_URL}/buzz/viewBuzz"


class DashboardPage(BasePage):
    WIDGET_HEADER = (By.CSS_SELECTOR, ".orangehrm-dashboard-widget-header")

    def navigate(self):
        self.driver.get(DASHBOARD_URL)
        self.find(self.WIDGET_HEADER)

    def get_widget_titles(self):
        def _read(d):
            titles = [w.text for w in d.find_elements(*self.WIDGET_HEADER) if w.text]
            return titles or False

        return self.wait.until(_read)


class DirectoryPage(BasePage):
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/../..//input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    DIRECTORY_CARD = (By.CSS_SELECTOR, ".orangehrm-directory-card")

    def navigate(self):
        self.driver.get(DIRECTORY_URL)
        self.find(self.EMPLOYEE_NAME_INPUT)

    def search_by_name_letter(self, letter):
        self.pick_first_autocomplete_option(self.EMPLOYEE_NAME_INPUT, letter)
        self.click(self.SEARCH_BUTTON)

    def get_result_cards(self):
        def _read(d):
            cards = d.find_elements(*self.DIRECTORY_CARD)
            return cards or False

        return self.wait.until(_read)


class BuzzPage(BasePage):
    POST_TEXTAREA = (By.CSS_SELECTOR, "textarea")
    POST_BUTTON = (By.XPATH, "//button[normalize-space()='Post']")
    FEED_POST = (By.CSS_SELECTOR, ".orangehrm-buzz-post-body-text")

    def navigate(self):
        self.driver.get(BUZZ_URL)
        self.find(self.POST_TEXTAREA)

    def create_post(self, text):
        self.type_text(self.POST_TEXTAREA, text)
        self.click(self.POST_BUTTON)

    def wait_until_post_appears_in_feed(self, expected_text):
        def _found(d):
            return any(expected_text in p.text for p in d.find_elements(*self.FEED_POST))

        self.wait.until(_found)
