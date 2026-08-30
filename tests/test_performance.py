import uuid

from pages.performance_page import PerformancePage


def test_add_kpi_succeeds(logged_in_driver):
    page = PerformancePage(logged_in_driver)
    page.navigate_to_kpi_list()
    toast_text = page.add_kpi(name=f"QA KPI {uuid.uuid4().hex[:6]}")
    assert "Success" in toast_text
