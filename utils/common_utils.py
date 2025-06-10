import configparser
import datetime
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import get_logger

logger = get_logger(__name__)


class CommonUtils:
    def __init__(self, driver):
        self.remote_driver = driver
        self.wait = WebDriverWait(driver, 15)

    def wait_for_element_clickable(self, locator):
        logger.info(f"Waiting for element to be clickable: {locator}")
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_visible(self, locator):
        logger.info(f"Waiting for element to be visible: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_all_elements_visible(self, locator):
        logger.info(f"Waiting for all elements to be visible: {locator}")
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_for_element_present(self, locator):
        logger.info(f"Waiting for element to be present: {locator}")
        return self.wait.until(EC.presence_of_element_located(locator))

    def scroll_into_view(self, element):
        logger.info("Scrolling into view")
        self.remote_driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_bottom(self):
        logger.info("Scrolling to bottom of the page")
        self.remote_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def take_screenshot(self, file_path):
        logger.info(f"Taking screenshot: {file_path}")
        self.remote_driver.save_screenshot(file_path)

    @staticmethod
    def get_url(key):
        url_config = configparser.ConfigParser()
        url_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'url_config.properties')
        url_config.read(url_path)
        logger.info(f"Fetching URL for key: {key}")
        return url_config['DEFAULT'].get(key)

    @staticmethod
    def get_locator(section, key):
        locator_config = configparser.ConfigParser()
        locator_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'locator_config.properties')
        locator_config.read(locator_path)
        logger.info(f"Fetching locator for section: {section}, key: {key}")
        return locator_config[section].get(key)

    def select_date(self, section, date_str):
        logger.info(f"Selecting date {date_str} for section: {section}")
        day, month, year = map(int, date_str.split("-"))
        target_month_year = datetime.date(year, month, day).strftime("%B %Y")

        CALENDAR_HEADER = (By.XPATH, CommonUtils.get_locator("COMMONS", "calendar_header"))
        NEXT_MONTH_BTN = (By.XPATH, CommonUtils.get_locator("COMMONS", "next_month_btn"))
        DATE_BTN = (By.XPATH, CommonUtils.get_locator(section, f"{section.lower()}_date_btn"))

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
            logger.error(f"Failed to select date {date_str}: {e}", exc_info=True)
            raise Exception(f"Failed to select date {date_str}: {e}")

    def select_list_item(self, city_name):
        logger.info(f"Selecting city from list: {city_name}")
        CITY_SUGGESTIONLIST = (By.XPATH, self.get_locator("COMMONS", "city_suggestionlist"))
        cities = self.wait_for_all_elements_visible(CITY_SUGGESTIONLIST)
        try:
            for city in cities:
                if city.text.strip().lower() == city_name.strip().lower():
                    city.click()
                    logger.info(f"Selected city: {city_name}")
                    return
            logger.warning(f"City not found in suggestion list: {city_name}")
        except Exception as e:
            logger.error(f"City '{city_name}' not found in suggestion list: {e}", exc_info=True)
            raise Exception(f"City '{city_name}' not found in suggestionlist: {e}")
