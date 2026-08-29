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

    def delete_first_result(self):
        self.click(self.ROW_CHECKBOX)
        self.click(self.DELETE_SELECTED_BUTTON)
        self.click(self.CONFIRM_DELETE_BUTTON)
