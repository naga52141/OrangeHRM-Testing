from config import LOGIN_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from pages.login_page import LoginPage


def test_valid_login_shows_dashboard(driver):
    driver.get(LOGIN_URL)
    login_page = LoginPage(driver)
    login_page.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    assert login_page.is_logged_in()


def test_invalid_login_shows_error(driver):
    driver.get(LOGIN_URL)
    login_page = LoginPage(driver)
    login_page.login("invalid_user", "wrong_password")
    assert "Invalid credentials" in login_page.get_error_text()
