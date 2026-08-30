import uuid

from pages.pim_page import PimPage


def test_add_search_delete_employee(logged_in_driver):
    page = PimPage(logged_in_driver)
    last_name = f"QA{uuid.uuid4().hex[:6]}"

    page.navigate()
    employee_id = page.add_employee(first_name="Automated", last_name=last_name)
    assert employee_id

    page.navigate()
    page.search_by_employee_id(employee_id)
    assert page.get_records_found_count() == 1

    toast_text = page.delete_first_result()
    assert "Success" in toast_text
    # Check the already-filtered list in place rather than re-navigating and
    # re-searching, which would race the page's own default (unfiltered)
    # fetch on load.
    assert page.has_no_records()


def test_employee_search_with_no_match_shows_no_records(logged_in_driver):
    page = PimPage(logged_in_driver)
    page.navigate()
    page.search_by_employee_id(f"NOPE{uuid.uuid4().hex[:6]}")
    assert page.has_no_records()
