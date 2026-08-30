from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage

SUBMIT_CLAIM_URL = f"{BASE_URL}/claim/submitClaim"


class ClaimPage(BasePage):
    EVENT_DROPDOWN_INDEX = 0
    CURRENCY_DROPDOWN_INDEX = 1
    REMARKS_INPUT = (By.XPATH, "//label[text()='Remarks']/../..//textarea")
    CREATE_BUTTON = (By.XPATH, "//button[normalize-space()='Create']")
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")

    def navigate(self):
        self.driver.get(SUBMIT_CLAIM_URL)
        self.find((By.CSS_SELECTOR, ".oxd-select-text"))

    def submit_claim(self, remarks):
        self.select_custom_dropdown_first_option(self.EVENT_DROPDOWN_INDEX)
        self.select_custom_dropdown_first_option(self.CURRENCY_DROPDOWN_INDEX)
        self.type_text(self.REMARKS_INPUT, remarks)
        self.click(self.CREATE_BUTTON)

        def _read_toast(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        return self.wait.until(_read_toast)
