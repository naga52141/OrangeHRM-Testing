import uuid

from pages.pim_page import PimPage


def test_add_employee_appears_in_directory(logged_in_driver):
    page = PimPage(logged_in_driver)
    last_name = f"QA{uuid.uuid4().hex[:6]}"

    page.navigate()
    employee_id = page.add_employee(first_name="Automated", last_name=last_name)
    assert employee_id

    page.navigate()
    page.search_by_employee_id(employee_id)
    assert page.get_records_found_count() == 1


def test_employee_search_with_no_match_shows_no_records(logged_in_driver):
    page = PimPage(logged_in_driver)
    page.navigate()
    page.search_by_employee_id(f"NOPE{uuid.uuid4().hex[:6]}")
    assert page.has_no_records()
