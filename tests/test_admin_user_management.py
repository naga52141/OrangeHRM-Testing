import uuid

from pages.admin_user_page import AdminUserPage


def test_add_search_delete_user(logged_in_driver):
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

    page.delete_first_result()
    assert page.get_text(page.TOAST_MESSAGE)

    page.navigate()
    page.search_by_username(unique_username)
    assert page.has_no_records()


def test_search_with_no_matching_username_shows_no_records(logged_in_driver):
    page = AdminUserPage(logged_in_driver)
    page.navigate()
    page.search_by_username(f"nonexistent_{uuid.uuid4().hex[:8]}")
    assert page.has_no_records()
