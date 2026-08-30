from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL
from pages.base_page import BasePage

CANDIDATES_URL = f"{BASE_URL}/recruitment/viewCandidates"


class RecruitmentPage(BasePage):
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/../..//input")
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")

    CANDIDATE_NAME_SEARCH_INPUT = (By.XPATH, "//label[text()='Candidate Name']/../..//input")
    KEYWORDS_SEARCH_INPUT = (By.XPATH, "//label[text()='Keywords']/../..//input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    RECORDS_FOUND_TEXT = (By.XPATH, "//span[contains(.,'Record Found') or contains(.,'Records Found')]")
    NO_RECORDS_TEXT = (By.XPATH, "//span[normalize-space(.)='No Records Found']")

    ROW_DELETE_ICON = (By.CSS_SELECTOR, ".oxd-table-row .bi-trash")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Yes, Delete']")
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")

    def navigate(self):
        self.driver.get(CANDIDATES_URL)
        self.find(self.RECORDS_FOUND_TEXT)

    def add_candidate(self, first_name, last_name, email):
        self.click(self.ADD_BUTTON)
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.EMAIL_INPUT, email)
        self.click(self.SAVE_BUTTON)
        self.wait.until(EC.url_contains("addCandidate"))

    def search_by_name(self, name_search_letters):
        self.pick_first_autocomplete_option(self.CANDIDATE_NAME_SEARCH_INPUT, name_search_letters)
        self.settle_after_filter_input()
        self.click(self.SEARCH_BUTTON)

    def search_by_keyword(self, keyword):
        self.type_text(self.KEYWORDS_SEARCH_INPUT, keyword)
        self.settle_after_filter_input()
        self.click(self.SEARCH_BUTTON)

    def get_records_found_count(self):
        text = self.get_text(self.RECORDS_FOUND_TEXT)
        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else 0

    def has_no_records(self):
        return self.is_visible(self.NO_RECORDS_TEXT)

    def delete_first_result(self):
        self.click(self.ROW_DELETE_ICON)
        self.click(self.CONFIRM_DELETE_BUTTON)

        def _read_toast(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        toast_text = self.wait.until(_read_toast)
        self.settle_after_filter_input()
        return toast_text
