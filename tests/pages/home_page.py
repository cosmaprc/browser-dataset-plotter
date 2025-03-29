from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def open_page(self, url):
        self.driver.get(url)

    def verify_successful_home_page_loading(self):
        try:
            header = self.driver.find_element(By.ID, "pandas-plot-viewer")
            return header.is_displayed()
        except NoSuchElementException as exc:
            raise AssertionError(
                "Header pandas-plot-viewer does not exist."
            ) from exc
