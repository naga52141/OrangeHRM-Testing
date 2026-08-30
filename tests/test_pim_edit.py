import uuid

from pages.pim_page import PimPage


def test_edit_contact_details_city_persists(logged_in_driver):
    page = PimPage(logged_in_driver)
    page.navigate()
    page.add_employee(first_name="Automated", last_name=f"Edit{uuid.uuid4().hex[:6]}")

    city_value = f"TestCity{uuid.uuid4().hex[:6]}"
    toast_text = page.edit_contact_details_city(city_value)
    assert "Success" in toast_text

    assert page.get_contact_details_city() == city_value
