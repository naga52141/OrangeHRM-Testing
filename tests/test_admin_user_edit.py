import uuid

from pages.admin_user_page import AdminUserPage


def test_edit_user_status_persists(logged_in_driver):
    page = AdminUserPage(logged_in_driver)
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"

    page.navigate()
    page.add_user(
        user_role="ESS",
        employee_search_letter="a",
        status="Enabled",
        username=unique_username,
        password="Str0ngP@ss!",
    )

    page.navigate()
    page.search_by_username(unique_username)
    assert page.get_records_found_count() == 1

    edit_toast = page.edit_first_result_status("Disabled")
    assert "Success" in edit_toast

    page.navigate()
    page.search_by_username(unique_username)
    assert "Disabled" in page.get_first_row_text()

    page.delete_first_result()
