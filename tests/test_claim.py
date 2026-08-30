from pages.claim_page import ClaimPage


def test_submit_claim_succeeds(logged_in_driver):
    page = ClaimPage(logged_in_driver)
    page.navigate()
    toast_text = page.submit_claim(remarks="Automated test claim")
    assert "Success" in toast_text
