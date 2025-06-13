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
    ROOM_RADIOBTN = (By.XPATH, CommonUtils.get_locator(section, "room_radiobtn"))
    CITY_BOX = (By.ID, CommonUtils.get_locator(section, "city_box"))
    CITY_TEXTBOX = (By.XPATH, CommonUtils.get_locator(section, "city_textbox"))
    HOTEL_CITY_SUGGESTIONLIST = (By.XPATH, CommonUtils.get_locator(section, "hotel_city_suggestionlist"))
    CHECKIN_DROPDOWN = (By.ID, CommonUtils.get_locator(section, "checkin_dropdown"))
    CHECKOUT_DROPDOWN = (By.ID, CommonUtils.get_locator(section, "checkout_dropdown"))
    ROOMS_GUESTS_DROPDOWN = (By.ID, CommonUtils.get_locator(section, "rooms_guests_dropdown"))
    ROOM_DROPDOWN = (By.XPATH, CommonUtils.get_locator(section, "room_dropdown"))
    ADULT_DROPDOWN = (By.XPATH, CommonUtils.get_locator(section, "adults_dropdown"))
    COUNT_BTN = (By.XPATH, CommonUtils.get_locator(section, "count_btn"))
    APPLY_BTN = (By.XPATH, CommonUtils.get_locator("COMMONS", "apply_btn"))
    SEARCH_BTN = (By.XPATH, CommonUtils.get_locator("COMMONS", "search_btn"))
    HOTEL_NAME_TEXT = (By.XPATH, CommonUtils.get_locator(section, "hotel_name_text"))
    HOTEL_LOCALITY_TEXT = (By.XPATH, CommonUtils.get_locator(section, "hotel_locality_text"))
    HOTEL_FARE_TEXT = (By.XPATH, CommonUtils.get_locator(section, "hotel_fare_text"))

    # Actions
    def select_room_type(self, room):
        try:
            logger.info(f"Selecting room type: {room}")
            self.utils.wait_for_element_visible(self.CLOSE_MODAL).click()
            self.utils.wait_for_element_clickable(self.ROOM_RADIOBTN).click()
        except Exception as e:
            logger.error(f"Error selecting room type('{room}'): {e}", exc_info=True)
            raise Exception(f"Error selecting room type('{room}'): {e}")

    def enter_location(self, location):
        try:
            logger.info(f"Entering hotel location: {location}")
            self.utils.wait_for_element_clickable(self.CITY_BOX).click()
            self.utils.wait_for_element_visible(self.CITY_TEXTBOX).send_keys(location)
            self.utils.select_list_item(self.section, location)
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
            self.utils.wait_for_element_visible(self.ROOM_DROPDOWN).click()
            count = self.utils.wait_for_all_elements_present(self.COUNT_BTN)
            for i in count:
                if i.text == rooms:
                    i.click()
                    break
            self.utils.wait_for_element_visible(self.ADULT_DROPDOWN).click()
            count = self.utils.wait_for_all_elements_present(self.COUNT_BTN)
            for i in count:
                if i.text == adults:
                    i.click()
                    break
            self.utils.wait_for_element_clickable(self.APPLY_BTN).click()
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
            logger.info("Capturing hotel search results")

            self.utils.wait_for_all_elements_present(self.HOTEL_NAME_TEXT)

            names = self.remote_driver.find_elements(*self.HOTEL_NAME_TEXT)
            localities = self.remote_driver.find_elements(*self.HOTEL_LOCALITY_TEXT)
            fares = self.remote_driver.find_elements(*self.HOTEL_FARE_TEXT)

            data = [["Name", "Locality", "Fare"]]
            num_rows = min(len(names), len(localities), len(fares))

            for i in range(num_rows):
                names = names[i].text.strip()
                localities = localities[i].text.strip()
                fares = fares[i].text.strip()

                logger.info(f"{names} | {localities} | {fares}")
                print(f"{names} | {localities} | {fares}")

                data.append([names, localities, fares])

            return data[1:]
        except Exception as e:
            logger.error(f"Error capturing hotel data: {e}", exc_info=True)
            raise Exception(f"Error capturing hotel data: {e}")
