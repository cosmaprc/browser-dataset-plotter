import pytest

from tests.pages.home_page import HomePage


@pytest.mark.home
def test_home_functionality(firefox_browser):
    """
    Test the Home functionality of the Datates Browser Plotter webapp
    """
    url = "http://localhost:8501"
    home_page = HomePage(firefox_browser)

    # Open Page
    home_page.open_page(url)

    assert home_page.verify_successful_home_page_loading()
