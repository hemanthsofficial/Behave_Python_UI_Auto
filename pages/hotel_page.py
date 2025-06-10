from selenium.webdriver.common.by import By
from utils.common_utils import CommonUtils
from utils.logger import get_logger

logger = get_logger(__name__)


class HotelPage:
    def __init__(self, driver):
        self.remote_driver = driver
        self.utils = CommonUtils(driver)

    # Locators
    section = "HOTEL_PAGE"
    CLOSE_MODAL = (By.XPATH, CommonUtils.get_locator("BASE_PAGE", "close_modal"))
    CITY_TEXTBOX = (By.ID, CommonUtils.get_locator(section, "city_textbox"))
    CITY_SUGGESTIONLIST = (By.XPATH, CommonUtils.get_locator("COMMONS", "city_suggestionlist"))
    CHECKIN_DROPDOWN = (By.ID, CommonUtils.get_locator(section, "checkin_dropdown"))
    CHECKOUT_DROPDOWN = (By.ID, CommonUtils.get_locator(section, "checkout_dropdown"))
    ROOMS_GUESTS_DROPDOWN = (By.XPATH, CommonUtils.get_locator(section, "rooms_guests_dropdown"))
    ROOM_DROPDOWN = CommonUtils.get_locator(section, "room_dropdown")
    ADULT_DROPDOWN = CommonUtils.get_locator(section, "adults_dropdown")
    APPLY_BTN = (By.XPATH, CommonUtils.get_locator("COMMONS", "apply_btn"))
    SEARCH_BTN = (By.XPATH, CommonUtils.get_locator("COMMONS", "search_btn"))
    HOTEL_NAMES = (By.XPATH, CommonUtils.get_locator(section, "hotel_names"))
    HOTEL_TARIFFS = (By.XPATH, CommonUtils.get_locator(section, "hotel_tariffs"))

    # Actions
    def enter_location(self, location):
        try:
            logger.info(f"Entering hotel location: {location}")
            self.utils.wait_for_element_visible(self.CLOSE_MODAL).click()
            self.utils.wait_for_element_clickable(self.CITY_TEXTBOX).click()
            self.utils.wait_for_element_visible(self.CITY_TEXTBOX).send_keys(location)
            self.utils.select_list_item(location)
        except Exception as e:
            logger.error(f"Error entering hotel location('{location}'): {e}", exc_info=True)
            raise Exception(f"Error entering hotel location('{location}'): {e}")

    def select_dates(self, checkin, checkout):
        try:
            logger.info(f"Selecting check-in: {checkin} and check-out: {checkout}")
            self.utils.wait_for_element_visible(self.CHECKIN_DROPDOWN).click()
            self.utils.select_date(self.section, checkin)
            self.utils.wait_for_element_visible(self.CHECKOUT_DROPDOWN).click()
            self.utils.select_date(self.section, checkout)
        except Exception as e:
            logger.error(f"Error selecting checkin('{checkin}')/checkout('{checkout}') dates: {e}", exc_info=True)
            raise Exception(f"Error selecting checkin('{checkin}')/checkout('{checkout}') dates: {e}")

    def select_room_and_guests(self, rooms, adults):
        try:
            logger.info(f"Selecting {rooms} room(s) and {adults} adult(s)")
            self.utils.wait_for_element_clickable(self.ROOMS_GUESTS_DROPDOWN).click()
            for _ in range(1, rooms):  # Default is 1
                self.remote_driver.find_element(By.XPATH, self.ROOM_DROPDOWN).click()
            for _ in range(1, adults):  # Default is 1
                self.remote_driver.find_element(By.XPATH, self.ADULT_DROPDOWN).click()
            self.remote_driver.find_element(*self.APPLY_BTN).click()
        except Exception as e:
            logger.error(f"Error selecting {rooms} room(s) and {adults} adult(s): {e}", exc_info=True)
            raise Exception(f"Error selecting {rooms} room(s) and {adults} adult(s): {e}")

    def click_search(self):
        try:
            logger.info("Clicking hotel search button")
            self.utils.wait_for_element_clickable(self.SEARCH_BTN).click()
        except Exception as e:
            logger.error(f"Error clicking hotel search button: {e}", exc_info=True)
            raise Exception(f"Error clicking hotel search button: {e}")

    def get_hotel_data(self):
        try:
            logger.info("Capturing hotel names and tariffs from search results")
            self.utils.wait_for_element_visible(self.HOTEL_NAMES)
            hotels = self.remote_driver.find_elements(*self.HOTEL_NAMES)
            tariffs = self.remote_driver.find_elements(*self.HOTEL_TARIFFS)
            hotel_data = []
            for i in range(min(len(hotels), len(tariffs))):
                name = hotels[i].text.strip()
                price = tariffs[i].text.strip()
                if name and price:
                    hotel_data.append([name, price])
            logger.info(f"Captured hotel data: {hotel_data}")
            return hotel_data
        except Exception as e:
            logger.error(f"Error capturing hotel data: {e}", exc_info=True)
            raise Exception(f"Error capturing hotel data: {e}")
