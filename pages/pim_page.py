from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import PIM_EMPLOYEE_LIST_URL
from pages.base_page import BasePage


class PimPage(BasePage):
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    EMPLOYEE_NAME_SEARCH_INPUT = (By.XPATH, "//label[text()='Employee Name']/../..//input")
    EMPLOYEE_ID_SEARCH_INPUT = (By.XPATH, "//label[text()='Employee Id']/../..//input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    EMPLOYEE_ID_VALUE = (By.XPATH, "//label[contains(text(),'Employee Id')]/../..//input")

    RECORDS_FOUND_TEXT = (By.XPATH, "//span[contains(.,'Record Found') or contains(.,'Records Found')]")
    NO_RECORDS_TEXT = (By.XPATH, "//span[normalize-space(.)='No Records Found']")
    EMPLOYEE_FULL_NAME_HEADER = (By.CSS_SELECTOR, ".employee-name")

    def navigate(self):
        self.driver.get(PIM_EMPLOYEE_LIST_URL)
        self.find(self.RECORDS_FOUND_TEXT)

    def add_employee(self, first_name, last_name):
        self.click(self.ADD_BUTTON)
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.click(self.SAVE_BUTTON)
        self.wait.until(EC.url_contains("viewPersonalDetails"))
        return self.get_attribute_when_populated(self.EMPLOYEE_ID_VALUE, "value")

    def search_by_name_letter(self, letter):
        picked_name = self.pick_first_autocomplete_option(self.EMPLOYEE_NAME_SEARCH_INPUT, letter)
        self.click(self.SEARCH_BUTTON)
        return picked_name

    def search_by_employee_id(self, employee_id):
        self.type_text(self.EMPLOYEE_ID_SEARCH_INPUT, employee_id)
        self.settle_after_filter_input()
        self.click(self.SEARCH_BUTTON)

    def get_records_found_count(self):
        text = self.get_text(self.RECORDS_FOUND_TEXT)
        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else 0

    def has_no_records(self):
        return self.is_visible(self.NO_RECORDS_TEXT)
