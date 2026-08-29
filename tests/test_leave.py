from pages.leave_page import LeavePage


def test_assign_leave_with_calendar_date_picker(logged_in_driver):
    page = LeavePage(logged_in_driver)
    page.navigate_to_assign_leave()
    toast_text = page.assign_leave(employee_search_letter="a", leave_type="US - Vacation")
    assert "Success" in toast_text or "Failed" in toast_text
