from pages.misc_pages import DashboardPage


def test_dashboard_widgets_are_present(logged_in_driver):
    page = DashboardPage(logged_in_driver)
    page.navigate()
    titles = page.get_widget_titles()
    for expected in ("Time at Work", "My Actions", "Quick Launch", "Buzz Latest Posts"):
        assert expected in titles
