from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")

    def navigate(self):
        self.driver.get(BUZZ_URL)
        self.find(self.POST_TEXTAREA)

    def create_post(self, text):
        self.type_text(self.POST_TEXTAREA, text)
        self.click(self.POST_BUTTON)

    def wait_until_post_appears_in_feed(self, expected_text):
        def _found(d):
            return any(expected_text in p.text for p in d.find_elements(*self.FEED_POST))

        try:
            WebDriverWait(self.driver, 12).until(_found)
        except TimeoutException:
            # The post always saves server-side, but the feed's own client-side
            # re-render after posting is unreliable (verified: a hard reload
            # consistently shows it even when the live DOM never updates).
            # Reload once and check again rather than waiting longer for an
            # update that may never come.
            self.driver.get(BUZZ_URL)
            WebDriverWait(self.driver, 15).until(_found)

    def delete_post(self, post_text):
        # text() misses this text (split across nested elements/interpolation,
        # the same recurring node-splitting gotcha), so match on "." instead.
        text_el = self.find((By.XPATH, f"//*[contains(.,'{post_text}') and contains(@class,'body-text')]"))
        container = text_el.find_element(
            By.XPATH, "./ancestor::div[contains(@class,'orangehrm-buzz-post-body')]/.."
        )
        container.find_element(By.CSS_SELECTOR, ".bi-three-dots").click()
        self.click((By.XPATH, "//p[normalize-space()='Delete Post']"))
        self.click((By.XPATH, "//button[normalize-space()='Yes, Delete']"))

        def _read_toast(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        return self.wait.until(_read_toast)
