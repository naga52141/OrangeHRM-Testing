import uuid

from pages.claim_page import ClaimPage


def test_submit_and_cancel_claim(logged_in_driver):
    page = ClaimPage(logged_in_driver)
    remarks = f"Automated test claim {uuid.uuid4().hex[:8]}"

    page.navigate()
    submit_toast = page.submit_claim(remarks=remarks)
    assert "Success" in submit_toast

    cancel_toast = page.cancel_claim_by_remarks(remarks)
    assert "Success" in cancel_toast
