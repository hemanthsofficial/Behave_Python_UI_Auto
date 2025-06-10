from selenium.webdriver.common.by import By

from utils.logger import get_logger
from utils.common_utils import CommonUtils

logger = get_logger(__name__)


class FlightPage:
    def __init__(self, driver):
        self.remote_driver = driver
        self.utils = CommonUtils(driver)

    # Locators
    section = "FLIGHT_PAGE"
    CLOSE_MODAL = (By.XPATH, CommonUtils.get_locator("BASE_PAGE", "close_modal"))
    TRIP_RADIOBTN = (By.XPATH, CommonUtils.get_locator(section, "trip_radiobtn"))
    FROM_TEXTBOX = (By.ID, CommonUtils.get_locator(section, "from_textbox"))
    TO_TEXTBOX = (By.ID, CommonUtils.get_locator(section, "to_textbox"))
    DEPARTURE_DROPDOWN = (By.ID, CommonUtils.get_locator(section, "departure_dropdown"))
    RETURN_DROPDOWN = (By.ID, CommonUtils.get_locator(section, "return_dropdown"))
    TRAVELLERS_CLASS_DROPDOWN = (By.ID, CommonUtils.get_locator(section, "travellers_class_dropdown"))
    ADULTS_BTN = (By.XPATH, CommonUtils.get_locator(section, "adults_btn"))
    CLASS_BTN = (By.XPATH, CommonUtils.get_locator(section, "class_btn"))
    APPLY_BTN = (By.XPATH, CommonUtils.get_locator("COMMONS", "apply_btn"))
    SEARCH_BTN = (By.XPATH, CommonUtils.get_locator("COMMONS", "search_btn"))
    SEARCH_RESULT = (By.XPATH, CommonUtils.get_locator(section, "search_result"))

    # actions
    def select_trip_type(self, trip):
        try:
            logger.info(f"Selecting trip type: {trip}")
            self.utils.wait_for_element_visible(self.CLOSE_MODAL).click()
            self.utils.wait_for_element_clickable(self.TRIP_RADIOBTN).click()
        except Exception as e:
            logger.error(f"Error selecting trip type('{trip}'): {e}", exc_info=True)
            raise Exception(f"Error selecting trip type('{trip}'): {e}")

    def enter_from_to_city(self, source, destination):
        try:
            logger.info(f"Entering source city: {source}")
            self.utils.wait_for_element_clickable(self.FROM_TEXTBOX).click()
            self.utils.wait_for_element_visible(self.FROM_TEXTBOX).send_keys(source)
            self.utils.select_list_item(source)

            logger.info(f"Entering destination city: {destination}")
            self.utils.wait_for_element_clickable(self.TO_TEXTBOX).click()
            self.utils.wait_for_element_visible(self.TO_TEXTBOX).send_keys(destination)
            self.utils.select_list_item(destination)
        except Exception as e:
            logger.error(f"Error entering source('{source}')/destination('{destination}'): {e}", exc_info=True)
            raise Exception(f"Error entering source('{source}')/destination('{destination}'): {e}")

    def select_dates(self, departure_date):
        try:
            logger.info(f"Selecting departure date: {departure_date}")
            self.utils.wait_for_element_visible(self.DEPARTURE_DROPDOWN).click()
            self.utils.select_date(self.section, departure_date)
        except Exception as e:
            logger.error(f"Error selecting departure date('{departure_date}'): {e}", exc_info=True)
            raise Exception(f"Error selecting departure date('{departure_date}'): {e}")

    def select_travellers_and_class(self, adults, travel_class):
        try:
            logger.info(f"Selecting travellers: {adults} and class: {travel_class}")
            self.utils.wait_for_element_clickable(self.TRAVELLERS_CLASS_DROPDOWN).click()
            self.utils.wait_for_all_elements_visible(self.ADULTS_BTN)[1].click()
            self.utils.wait_for_all_elements_visible(self.CLASS_BTN)[3].click()
            self.utils.wait_for_element_visible(self.APPLY_BTN).click()
        except Exception as e:
            logger.error(f"Error selecting travellers('{adults}')/class('{travel_class}'): {e}", exc_info=True)
            raise Exception(f"Error selecting travellers('{adults}')/class('{travel_class}'): {e}")

    def click_search(self):
        try:
            logger.info("Clicking the search button")
            self.utils.wait_for_element_clickable(self.SEARCH_BTN).click()
        except Exception as e:
            logger.error(f"Error clicking flight search button: {e}", exc_info=True)
            raise Exception(f"Error clicking flight search button: {e}")

    def get_flight_names(self):
        try:
            logger.info("Capturing flight names from search results")
            elements = self.utils.wait_for_all_elements_visible(self.SEARCH_RESULT)
            flights = list(set([e.text.strip() for e in elements if e.text.strip()]))
            logger.info(f"Captured flights: {flights}")
            return flights
        except Exception as e:
            logger.error(f"Error capturing flight data: {e}", exc_info=True)
            raise Exception(f"Error capturing flight data: {e}")
