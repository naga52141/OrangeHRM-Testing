import uuid

from pages.misc_pages import BuzzPage


def test_create_post_appears_in_feed(logged_in_driver):
    page = BuzzPage(logged_in_driver)
    page.navigate()
    unique_text = f"Automated test post {uuid.uuid4().hex[:8]}"
    page.create_post(unique_text)
    page.wait_until_post_appears_in_feed(unique_text)
