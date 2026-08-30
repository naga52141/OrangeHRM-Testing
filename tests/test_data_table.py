from pages.admin_user_page import AdminUserPage
from pages.pim_page import PimPage


def test_pagination_changes_visible_rows(logged_in_driver):
    page = PimPage(logged_in_driver)
    page.navigate()
    page_1_first_row = page.get_first_row_text()

    page.go_to_page(2)
    page_2_first_row = page.get_first_row_text()

    assert page_1_first_row != page_2_first_row


def test_sorting_by_column_changes_row_order(logged_in_driver):
    page = PimPage(logged_in_driver)
    page.navigate()
    before_sort = page.get_first_row_text()

    # column index 2 = "First (& Middle) Name"
    page.sort_by_column(column_index=2, direction="Descending")
    after_sort = page.get_first_row_text()

    assert before_sort != after_sort


def test_admin_users_sorting_changes_row_order(logged_in_driver):
    page = AdminUserPage(logged_in_driver)
    page.navigate()
    before_sort = page.get_first_row_text()

    # column index 1 = "Username" (index 0 is the select-all checkbox column)
    page.sort_by_column(column_index=1, direction="Descending")
    after_sort = page.get_first_row_text()

    assert before_sort != after_sort
