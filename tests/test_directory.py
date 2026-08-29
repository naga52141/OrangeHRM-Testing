from pages.misc_pages import DirectoryPage


def test_directory_search_returns_results(logged_in_driver):
    page = DirectoryPage(logged_in_driver)
    page.navigate()
    page.search_by_name_letter("a")
    cards = page.get_result_cards()
    assert len(cards) > 0
