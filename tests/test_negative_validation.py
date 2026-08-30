import uuid

from pages.admin_user_page import AdminUserPage
from pages.pim_page import PimPage
from pages.recruitment_page import RecruitmentPage


def test_add_user_rejects_mismatched_passwords(logged_in_driver):
    page = AdminUserPage(logged_in_driver)
    page.navigate()
    page.click(page.ADD_BUTTON)
    page.select_custom_dropdown(page.USER_ROLE_DROPDOWN_INDEX, "ESS")
    page.pick_first_autocomplete_option(page.EMPLOYEE_NAME_INPUT, "a")
    page.select_custom_dropdown(page.STATUS_DROPDOWN_INDEX, "Enabled")
    page.type_text(page.USERNAME_INPUT, f"testuser_{uuid.uuid4().hex[:8]}")
    page.type_text(page.PASSWORD_INPUT, "Str0ngP@ss!")
    page.type_text(page.CONFIRM_PASSWORD_INPUT, "ADifferentPassword!")
    page.click(page.SAVE_BUTTON)

    errors = page.get_field_errors()
    assert any("match" in e.lower() for e in errors)


def test_add_employee_rejects_empty_required_fields(logged_in_driver):
    page = PimPage(logged_in_driver)
    page.navigate()
    page.click(page.ADD_BUTTON)
    page.click(page.SAVE_BUTTON)

    errors = page.get_field_errors()
    # The auto-suggested Employee Id can occasionally collide under
    # concurrent load, adding an unrelated "already exists" error - assert
    # on the required-field behavior being tested, not on every error present.
    required_errors = [e for e in errors if "required" in e.lower()]
    assert len(required_errors) >= 2


def test_add_candidate_rejects_invalid_email_format(logged_in_driver):
    page = RecruitmentPage(logged_in_driver)
    page.navigate()
    page.click(page.ADD_BUTTON)
    page.type_text(page.FIRST_NAME_INPUT, "Automated")
    page.type_text(page.LAST_NAME_INPUT, f"QA{uuid.uuid4().hex[:6]}")
    page.type_text(page.EMAIL_INPUT, "not-an-email")
    page.click(page.SAVE_BUTTON)

    errors = page.get_field_errors()
    assert any("format" in e.lower() for e in errors)
