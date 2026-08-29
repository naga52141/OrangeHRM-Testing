import pytest

from pages.app_shell_page import AppShellPage

# (nav label, expected substring in the resulting URL, expected header text)
# Verified against the live demo: each module's h6 header matches its own
# nav label, except My Info (lands on a PIM personal-details page).
NAV_ITEMS = [
    ("Admin", "admin/viewSystemUsers", "Admin"),
    ("PIM", "pim/viewEmployeeList", "PIM"),
    ("Leave", "leave/viewLeaveList", "Leave"),
    ("Time", "time/viewEmployeeTimesheet", "Time"),
    ("Recruitment", "recruitment/viewCandidates", "Recruitment"),
    ("My Info", "pim/viewPersonalDetails", "PIM"),
    ("Performance", "performance/searchEvaluatePerformanceReview", "Performance"),
    ("Dashboard", "dashboard/index", "Dashboard"),
    ("Directory", "directory/viewDirectory", "Directory"),
    ("Claim", "claim/viewAssignClaim", "Claim"),
    ("Buzz", "buzz/viewBuzz", "Buzz"),
]


@pytest.mark.parametrize("nav_label, url_fragment, expected_header", NAV_ITEMS)
def test_nav_item_opens_correct_page(logged_in_driver, nav_label, url_fragment, expected_header):
    page = AppShellPage(logged_in_driver)
    page.click_nav_item(nav_label)
    page.wait.until(lambda d: url_fragment in d.current_url)
    assert expected_header in page.get_page_headers()


def test_maintenance_nav_item_requires_admin_reauth(logged_in_driver):
    page = AppShellPage(logged_in_driver)
    page.click_nav_item("Maintenance")
    page.wait.until(lambda d: "maintenance" in d.current_url)
    assert page.is_visible(page.MAINTENANCE_USERNAME_INPUT)
    assert page.is_visible(page.MAINTENANCE_PASSWORD_INPUT)
    assert page.is_visible(page.MAINTENANCE_CONFIRM_BUTTON)


def test_user_dropdown_shows_account_menu(logged_in_driver):
    page = AppShellPage(logged_in_driver)
    menu_items = page.get_user_dropdown_menu_items()
    for expected in ("About", "Support", "Change Password", "Logout"):
        assert expected in menu_items


def test_logout_returns_to_login_page(logged_in_driver):
    page = AppShellPage(logged_in_driver)
    page.open_user_dropdown()
    page.click(page.LOGOUT_LINK)
    page.wait.until(lambda d: "auth/login" in d.current_url)
