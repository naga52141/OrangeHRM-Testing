import pytest

from config import LOGIN_URL
from pages.accessibility import scan, violations_by_impact
from pages.misc_pages import DashboardPage
from pages.admin_user_page import AdminUserPage

# "Critical" accessibility violations (axe-core's most severe category, e.g.
# a button with no discernible text) are asserted against as a genuine
# quality bar. Serious/moderate/minor findings are reported but not failed
# on - fixing every accessibility issue on a third-party public demo isn't
# in scope, but a critical one that blocks screen reader users is worth
# treating as a real finding, not noise.
#
# Dashboard and Admin Users are marked xfail: they currently DO have real
# critical violations in the live OrangeHRM demo (icon buttons and form
# inputs with no accessible name - confirmed via axe-core, not a bug in
# this suite). xfail tracks the known issue visibly in every report without
# turning the whole CI run red for a problem in someone else's app.


def _assert_no_critical_violations(driver, page_name):
    results = scan(driver)
    by_impact = violations_by_impact(results)
    print(f"\n{page_name} accessibility violations by impact: {by_impact}")
    assert "critical" not in by_impact, (
        f"{page_name} has critical accessibility violations: {by_impact.get('critical')}"
    )


def test_login_page_has_no_critical_accessibility_violations(driver):
    driver.get(LOGIN_URL)
    _assert_no_critical_violations(driver, "Login")


@pytest.mark.xfail(reason="Live app has a real critical violation: button-name (icon buttons with no accessible label)", strict=False)
def test_dashboard_has_no_critical_accessibility_violations(logged_in_driver):
    page = DashboardPage(logged_in_driver)
    page.navigate()
    _assert_no_critical_violations(logged_in_driver, "Dashboard")


@pytest.mark.xfail(reason="Live app has real critical violations: button-name, label (form inputs with no accessible name)", strict=False)
def test_admin_users_has_no_critical_accessibility_violations(logged_in_driver):
    page = AdminUserPage(logged_in_driver)
    page.navigate()
    _assert_no_critical_violations(logged_in_driver, "Admin Users")
