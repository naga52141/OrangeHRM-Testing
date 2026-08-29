import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text):
        def _type(d):
            try:
                el = d.find_element(*locator)
                el.clear()
                el.send_keys(text)
                return True
            except StaleElementReferenceException:
                return False

        def _value_stuck(d):
            return (d.find_element(*locator).get_attribute("value") or "") == text

        self.wait.until(_type)
        try:
            self.wait.until(_value_stuck)
        except TimeoutException:
            self.wait.until(_type)
            self.wait.until(_value_stuck)

    def settle_after_filter_input(self):
        # OrangeHRM's search forms re-render their internal filter state a beat after
        # the DOM input value updates. Submitting immediately can race an in-flight
        # default-list fetch and get the unfiltered results back. No DOM signal marks
        # this as done, so a short fixed wait is the practical workaround.
        time.sleep(1.5)

    def get_attribute_when_populated(self, locator, attribute):
        return self.wait.until(
            lambda d: d.find_element(*locator).get_attribute(attribute) or False
        )

    def get_text(self, locator):
        def _read(d):
            try:
                return d.find_element(*locator).text
            except StaleElementReferenceException:
                return False

        return self.wait.until(_read)

    def is_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    def select_custom_dropdown(self, dropdown_index, option_text):
        from selenium.webdriver.common.by import By

        dropdowns = self.wait.until(
            lambda d: d.find_elements(By.CSS_SELECTOR, ".oxd-select-text") or False
        )
        dropdowns[dropdown_index].click()
        option_xpath = (By.XPATH, f"//div[@role='listbox']//span[text()='{option_text}']")
        self.click(option_xpath)

    def pick_first_autocomplete_option(self, input_locator, search_text):
        from selenium.webdriver.common.by import By

        self.type_text(input_locator, search_text)
        first_option = (
            By.XPATH,
            "(//div[contains(@class,'oxd-autocomplete-dropdown')]//span)[1]",
        )
        option_text = self.get_text(first_option)
        normalized_option_text = " ".join(option_text.split())
        self.click(first_option)
        self.wait.until(
            lambda d: normalized_option_text
            in " ".join((d.find_element(*input_locator).get_attribute("value") or "").split())
        )
        return option_text
