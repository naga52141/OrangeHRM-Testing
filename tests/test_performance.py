import uuid

from pages.performance_page import PerformancePage


def test_add_and_delete_kpi(logged_in_driver):
    page = PerformancePage(logged_in_driver)
    kpi_name = f"QA KPI {uuid.uuid4().hex[:6]}"

    page.navigate_to_kpi_list()
    add_toast = page.add_kpi(name=kpi_name)
    assert "Success" in add_toast

    delete_toast = page.delete_kpi_by_name(kpi_name)
    assert "Success" in delete_toast
