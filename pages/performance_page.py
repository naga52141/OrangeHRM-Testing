from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage

ADD_KPI_URL = f"{BASE_URL}/performance/searchKpi"


class PerformancePage(BasePage):
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    KPI_NAME_INPUT = (By.XPATH, "//label[text()='Key Performance Indicator']/../..//input")
    JOB_TITLE_DROPDOWN_INDEX = 0
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")

    def navigate_to_kpi_list(self):
        self.driver.get(ADD_KPI_URL)
        self.find(self.ADD_BUTTON)

    def add_kpi(self, name):
        self.click(self.ADD_BUTTON)
        self.type_text(self.KPI_NAME_INPUT, name)
        self.select_custom_dropdown_first_option(self.JOB_TITLE_DROPDOWN_INDEX)
        self.click(self.SAVE_BUTTON)
        return self._read_toast()

    def delete_kpi_by_name(self, name):
        row_locator = (By.XPATH, f"//div[@role='row'][.//div[contains(text(),'{name}')]]")
        row = self.find(row_locator)
        row.find_element(By.CSS_SELECTOR, ".bi-trash").click()
        self.click((By.XPATH, "//button[normalize-space()='Yes, Delete']"))
        toast_text = self._read_toast()
        self.settle_after_filter_input()
        return toast_text

    def _read_toast(self):
        def _read(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        return self.wait.until(_read)
