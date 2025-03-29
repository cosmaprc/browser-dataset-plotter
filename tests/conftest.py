import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture()
def firefox_browser():
    # Configure Firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")

    # Download the GeckoDriver binary on the fly
    driver = webdriver.Firefox(
        options=options, service=FirefoxService(GeckoDriverManager().install())
    )

    driver.implicitly_wait(10)
    # Yield the WebDriver instance
    yield driver
    # Close the WebDriver instance
    driver.quit()
