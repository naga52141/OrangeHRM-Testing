import time

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

    EMPLOYEE_ID_VALUE = (By.XPATH, "//label[contains(.,'Employee Id')]/../..//input")

    RECORDS_FOUND_TEXT = (By.XPATH, "//span[contains(.,'Record Found') or contains(.,'Records Found')]")
    NO_RECORDS_TEXT = (By.XPATH, "//span[normalize-space(.)='No Records Found']")
    EMPLOYEE_FULL_NAME_HEADER = (By.CSS_SELECTOR, ".employee-name")

    ROW_DELETE_ICON = (By.CSS_SELECTOR, ".oxd-table-row .bi-trash")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Yes, Delete']")
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")

    TABLE_ROW = (By.CSS_SELECTOR, ".oxd-table-card")
    PAGINATION_ITEM = (By.CSS_SELECTOR, ".oxd-pagination-page-item")
    TABLE_HEADER_CELL = (By.CSS_SELECTOR, ".oxd-table-header-cell")
    HEADER_SORT_ICON = (By.CSS_SELECTOR, ".oxd-table-header-sort-icon")

    CONTACT_DETAILS_TAB = (By.XPATH, "//a[text()='Contact Details']")
    PERSONAL_DETAILS_TAB = (By.XPATH, "//a[text()='Personal Details']")
    CITY_INPUT = (By.XPATH, "//label[text()='City']/../..//input")

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

    def delete_first_result(self):
        self.click(self.ROW_DELETE_ICON)
        self.click(self.CONFIRM_DELETE_BUTTON)

        def _read_toast(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        toast_text = self.wait.until(_read_toast)
        # The delete toast can fire slightly before the backend finishes
        # removing the record, so an immediate re-search can still show it.
        self.settle_after_filter_input()
        return toast_text

    def get_first_row_text(self):
        def _read(d):
            rows = d.find_elements(*self.TABLE_ROW)
            return rows[0].text if rows else False

        return self.wait.until(_read)

    def go_to_page(self, page_number):
        self.find(self.TABLE_ROW)
        pages = self.wait.until(lambda d: d.find_elements(*self.PAGINATION_ITEM) or False)
        pages[page_number - 1].click()
        self.settle_after_filter_input()

    def sort_by_column(self, column_index, direction):
        self.find(self.TABLE_ROW)
        headers = self.wait.until(lambda d: d.find_elements(*self.TABLE_HEADER_CELL) or False)
        headers[column_index].find_element(*self.HEADER_SORT_ICON).click()

        def _visible_direction_option(d):
            options = d.find_elements(By.XPATH, f"//li[normalize-space()='{direction}']")
            visible = [o for o in options if o.is_displayed()]
            return visible or False

        self.wait.until(_visible_direction_option)[0].click()
        self.settle_after_filter_input()

    def edit_contact_details_city(self, city):
        self.click(self.CONTACT_DETAILS_TAB)
        self.type_text(self.CITY_INPUT, city)
        self.click(self.SAVE_BUTTON)

        def _read_toast(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        return self.wait.until(_read_toast)

    def get_contact_details_city(self):
        # The save toast fires optimistically - the value shows correctly in
        # the form immediately, but the actual backend commit measured up to
        # ~15s in testing. Navigating away before it lands doesn't just read
        # stale data, it appears to abandon the in-flight save outright
        # (value permanently empty after, confirmed via direct inspection,
        # not merely slow to appear). Wait for the commit before navigating
        # at all, whether via reload or in-app tabs.
        time.sleep(15)
        self.click(self.PERSONAL_DETAILS_TAB)
        self.click(self.CONTACT_DETAILS_TAB)
        return self.get_attribute_when_populated(self.CITY_INPUT, "value")
