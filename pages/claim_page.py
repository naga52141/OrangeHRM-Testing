from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage

SUBMIT_CLAIM_URL = f"{BASE_URL}/claim/submitClaim"
MY_CLAIMS_URL = f"{BASE_URL}/claim/viewClaim"


class ClaimPage(BasePage):
    EVENT_DROPDOWN_INDEX = 0
    CURRENCY_DROPDOWN_INDEX = 1
    REMARKS_INPUT = (By.XPATH, "//label[text()='Remarks']/../..//textarea")
    CREATE_BUTTON = (By.XPATH, "//button[normalize-space()='Create']")
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")

    ROW_VIEW_DETAILS_BUTTON = (By.XPATH, ".//button[normalize-space()='View Details']")
    CANCEL_CLAIM_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")

    def navigate(self):
        self.driver.get(SUBMIT_CLAIM_URL)
        self.find((By.CSS_SELECTOR, ".oxd-select-text"))

    def submit_claim(self, remarks):
        self.select_custom_dropdown_first_option(self.EVENT_DROPDOWN_INDEX)
        self.select_custom_dropdown_first_option(self.CURRENCY_DROPDOWN_INDEX)
        self.type_text(self.REMARKS_INPUT, remarks)
        self.click(self.CREATE_BUTTON)
        return self._read_toast()

    def cancel_claim_by_remarks(self, remarks):
        self.driver.get(MY_CLAIMS_URL)
        row_locator = (By.XPATH, f"//div[@role='row'][.//div[contains(.,'{remarks}')]]")
        row = self.find(row_locator)
        row.find_element(*self.ROW_VIEW_DETAILS_BUTTON).click()
        self.click(self.CANCEL_CLAIM_BUTTON)
        return self._read_toast()

    def _read_toast(self):
        def _read(d):
            texts = [e.text for e in d.find_elements(*self.TOAST_MESSAGE) if e.text]
            return " ".join(texts) or False

        return self.wait.until(_read)
