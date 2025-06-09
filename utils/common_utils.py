import configparser
import datetime
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CommonUtils:
    def __init__(self, driver):
        self.remote_driver = driver
        self.wait = WebDriverWait(driver, 15)

    # Waits
    def wait_for_element_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_all_elements_visible(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_for_element_present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    # Scroll
    def scroll_into_view(self, element):
        self.remote_driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_bottom(self):
        self.remote_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Screenshot
    def take_screenshot(self, file_path):
        self.remote_driver.save_screenshot(file_path)

    # url extractor
    @staticmethod
    def get_url(key):
        url_config = configparser.ConfigParser()
        url_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'url_config.properties')
        url_config.read(url_path)
        return url_config['DEFAULT'].get(key)

    # locator extractor
    @staticmethod
    def get_locator(section, key):
        locator_config = configparser.ConfigParser()
        locator_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'locator_config.properties')
        locator_config.read(locator_path)
        return locator_config[section].get(key)

    # date selection
    def select_date(self, section, date_str):
        day, month, year = map(int, date_str.split("-"))
        target_month_year = datetime.date(year, month, day).strftime("%B %Y")

        CALENDAR_HEADER = (By.XPATH, CommonUtils.get_locator("COMMONS", "calendar_header"))
        NEXT_MONTH_BTN = (By.XPATH, CommonUtils.get_locator("COMMONS", "next_month_btn"))
        if section == "FLIGHT_PAGE":
            DATE_BTN = (By.XPATH, CommonUtils.get_locator("FLIGHT_PAGE", "flight_date_btn"))
        if section == "HOTEL_PAGE":
            DATE_BTN = (By.XPATH, CommonUtils.get_locator("HOTEL_PAGE", "hotel_date_btn"))

        try:
            while True:
                calendar_header = self.wait_for_element_visible(CALENDAR_HEADER)
                current_month_year = calendar_header.text.strip()
                if current_month_year == target_month_year:
                    date_btn = self.wait_for_element_clickable(DATE_BTN)
                    self.scroll_into_view(date_btn)
                    date_btn.click()
                    break
                else:
                    next_month_btn = self.wait_for_element_clickable(NEXT_MONTH_BTN)
                    next_month_btn.click()

        except Exception as e:
            raise Exception(f"Failed to select date {date_str}: {e}")

    # select list item
    def select_list_item(self, city_name):
        CITY_SUGGESTIONLIST = (By.XPATH, self.get_locator("COMMONS", "city_suggestionlist"))
        cities = self.wait_for_all_elements_visible(CITY_SUGGESTIONLIST)
        try:
            for city in cities:
                if city.text.strip().lower() == city_name.strip().lower():
                    city.click()
                    return
        except Exception as e:
            raise Exception(f"City '{city_name}' not found in suggestionlist: {e}")
