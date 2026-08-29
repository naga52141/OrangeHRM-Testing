from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AppShellPage(BasePage):
    USER_DROPDOWN_TAB = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    DROPDOWN_MENU_ITEM = (By.CSS_SELECTOR, ".oxd-dropdown-menu li a")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout']")

    MAINTENANCE_USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/../..//input")
    MAINTENANCE_PASSWORD_INPUT = (By.XPATH, "//label[text()='Password']/../..//input[@type='password']")
    MAINTENANCE_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space()='Confirm']")

    def nav_item_locator(self, name):
        return (By.XPATH, f"//a[.//span[text()='{name}']]")

    def click_nav_item(self, name):
        self.click(self.nav_item_locator(name))

    def get_page_headers(self):
        def _read(d):
            headers = [h.text for h in d.find_elements(By.CSS_SELECTOR, "h6") if h.text]
            return headers or False

        return self.wait.until(_read)

    def open_user_dropdown(self):
        self.click(self.USER_DROPDOWN_TAB)

    def get_user_dropdown_menu_items(self):
        self.open_user_dropdown()

        def _read(d):
            items = [i.text for i in d.find_elements(*self.DROPDOWN_MENU_ITEM) if i.text]
            return items or False

        return self.wait.until(_read)
