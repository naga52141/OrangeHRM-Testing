from pages.admin_user_page import AdminUserPage


def test_selecting_multiple_rows_updates_selected_count(logged_in_driver):
    page = AdminUserPage(logged_in_driver)
    page.navigate()

    page.select_first_n_rows(2)
    assert "2" in page.get_selected_count_text()

    assert page.is_visible(page.DELETE_SELECTED_BUTTON)
