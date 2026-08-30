from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import ADMIN_USERS_URL
from pages.base_page import BasePage


class AdminUserPage(BasePage):
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    USER_ROLE_DROPDOWN_INDEX = 0
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/../..//input")
    STATUS_DROPDOWN_INDEX = 1
    USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/../..//input")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Password']/../..//input[@type='password']")
    CONFIRM_PASSWORD_INPUT = (
        By.XPATH,
        "//label[text()='Confirm Password']/../..//input[@type='password']",
    )

    SEARCH_USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/../..//input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.CSS_SELECTOR, "button[type='reset']")

    RECORDS_FOUND_TEXT = (By.XPATH, "//span[contains(.,'Record Found') or contains(.,'Records Found')]")
    TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-card")
    ROW_CHECKBOX = (By.CSS_SELECTOR, ".oxd-table-row .oxd-checkbox-input")
    ROW_EDIT_ICON = (By.CSS_SELECTOR, ".oxd-table-row .bi-pencil-fill")
    DELETE_SELECTED_BUTTON = (By.XPATH, "//button[normalize-space()='Delete Selected']")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Yes, Delete']")
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")
    NO_RECORDS_TEXT = (By.XPATH, "//span[normalize-space(.)='No Records Found']")

    def navigate(self):
        self.driver.get(ADMIN_USERS_URL)
        self.find(self.RECORDS_FOUND_TEXT)

    def add_user(self, user_role, employee_search_letter, status, username, password):
        self.click(self.ADD_BUTTON)
        self.select_custom_dropdown(self.USER_ROLE_DROPDOWN_INDEX, user_role)
        self.pick_first_autocomplete_option(self.EMPLOYEE_NAME_INPUT, employee_search_letter)
        self.select_custom_dropdown(self.STATUS_DROPDOWN_INDEX, status)
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.type_text(self.CONFIRM_PASSWORD_INPUT, password)
        self.click(self.SAVE_BUTTON)
        self.wait.until(EC.url_contains("viewSystemUsers"))

    def search_by_username(self, username):
        self.type_text(self.SEARCH_USERNAME_INPUT, username)
        self.settle_after_filter_input()
        self.click(self.SEARCH_BUTTON)

    def reset_search(self):
        self.click(self.RESET_BUTTON)

    def get_records_found_count(self):
        text = self.get_text(self.RECORDS_FOUND_TEXT)
        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else 0

    def has_no_records(self):
        return self.is_visible(self.NO_RECORDS_TEXT)

    def get_first_row_text(self):
        def _read(d):
            rows = d.find_elements(*self.TABLE_ROWS)
            return rows[0].text if rows else False

        return self.wait.until(_read)

    def edit_first_result_status(self, new_status):
        self.click(self.ROW_EDIT_ICON)
        self.select_custom_dropdown(self.STATUS_DROPDOWN_INDEX, new_status)
        self.click(self.SAVE_BUTTON)

        # Check for the toast immediately, not after waiting for the URL to
        # change first - toasts here auto-dismiss, and that extra sequential
        # wait can mean it's already gone by the time we look.
        def _read_toast(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        toast_text = self.wait.until(_read_toast)
        self.wait.until(EC.url_contains("viewSystemUsers"))
        return toast_text

    def delete_first_result(self):
        self.click(self.ROW_CHECKBOX)
        self.click(self.DELETE_SELECTED_BUTTON)
        self.click(self.CONFIRM_DELETE_BUTTON)

        def _read_toast(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        toast_text = self.wait.until(_read_toast)
        self.settle_after_filter_input()
        return toast_text
