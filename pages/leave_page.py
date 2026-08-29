from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage

ASSIGN_LEAVE_URL = f"{BASE_URL}/leave/assignLeave"


class LeavePage(BasePage):
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/../..//input")
    LEAVE_TYPE_DROPDOWN_INDEX = 0
    FROM_DATE_INPUT = (By.XPATH, "//label[text()='From Date']/../..//input")
    TO_DATE_INPUT = (By.XPATH, "//label[text()='To Date']/../..//input")
    WORKING_DAY_CALENDAR_CELL = (
        By.XPATH,
        "//div[contains(@class,'oxd-calendar-date-wrapper') and "
        "not(contains(@class,'--non-working-day')) and not(contains(@class,'--disabled'))]"
        "//div[contains(@class,'oxd-calendar-date')]",
    )
    ASSIGN_BUTTON = (By.XPATH, "//button[normalize-space()='Assign']")
    CONFIRM_OK_BUTTON = (By.XPATH, "//button[normalize-space()='Ok']")
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")

    def navigate_to_assign_leave(self):
        self.driver.get(ASSIGN_LEAVE_URL)
        self.find(self.EMPLOYEE_NAME_INPUT)

    def pick_working_day(self, date_input_locator):
        self.click(date_input_locator)
        self.click(self.WORKING_DAY_CALENDAR_CELL)

    def assign_leave(self, employee_search_letter, leave_type):
        self.pick_first_autocomplete_option(self.EMPLOYEE_NAME_INPUT, employee_search_letter)
        self.select_custom_dropdown(self.LEAVE_TYPE_DROPDOWN_INDEX, leave_type)
        self.pick_working_day(self.FROM_DATE_INPUT)
        self.pick_working_day(self.TO_DATE_INPUT)
        self.click(self.ASSIGN_BUTTON)
        if self.is_visible(self.CONFIRM_OK_BUTTON):
            self.click(self.CONFIRM_OK_BUTTON)

        def _read_toast(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        return self.wait.until(_read_toast)
