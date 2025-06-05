from selenium.webdriver.common.by import By

from utils.common_utils import CommonUtils


class HotelPage:
    def __init__(self, driver):
        self.driver = driver
        self.utils = CommonUtils(driver)

    # Locators
    section = "HOTEL_PAGE"
    LOCATION_INPUT_BOX = (By.XPATH, CommonUtils.get_locator(section, "location_input_box"))
    FIRST_SUGGESTION = (By.XPATH, CommonUtils.get_locator(section, "first_suggestion"))
    SEARCH_BUTTON = (By.XPATH, CommonUtils.get_locator(section, "search_button"))
    HOTEL_NAMES = (By.XPATH, CommonUtils.get_locator(section, "hotel_names"))
    HOTEL_TARIFFS = (By.XPATH, CommonUtils.get_locator(section, "hotel_tariffs"))
    GUEST_ROOM_BTN = (By.XPATH, CommonUtils.get_locator(section, "guest_room_btn"))
    ROOM_PLUS_BTN = CommonUtils.get_locator(section, "room_plus_btn")
    ADULT_PLUS_BTN = CommonUtils.get_locator(section, "adult_plus_btn")
    APPLY_GUEST_BTN = (By.XPATH, CommonUtils.get_locator(section, "apply_guest_btn"))

    # Actions
    def enter_location(self, location):
        try:
            self.utils.wait_for_element_clickable(self.LOCATION_INPUT_BOX).click()
            input_box = self.utils.wait_for_element_visible(self.LOCATION_INPUT_BOX)
            input_box.send_keys(location)
            self.utils.wait_for_element_clickable(self.FIRST_SUGGESTION).click()
        except Exception as e:
            raise Exception(f"Error entering hotel location('{location}'): {e}")

    def select_dates(self, checkin, checkout):
        try:
            self.utils.select_date(checkin)
            self.utils.select_date(checkout)
        except Exception as e:
            raise Exception(f"Error selecting checkin('{checkin}')/checkout('{checkout}') dates: {e}")

    def select_room_and_guests(self, rooms, adults):
        try:
            self.utils.wait_for_element_clickable(self.GUEST_ROOM_BTN).click()

            # Rooms selection
            for _ in range(1, rooms):  # Already 1 by default
                self.remote_driver.find_element(By.XPATH, self.ROOM_PLUS_BTN).click()

            # Adults selection
            for _ in range(1, adults):  # Already 1 by default
                self.remote_driver.find_element(By.XPATH, self.ADULT_PLUS_BTN).click()

            self.remote_driver.find_element(*self.APPLY_GUEST_BTN).click()
        except Exception as e:
            raise Exception(f"Error selecting {rooms} room(s) and {adults} adult(s): {e}")

    def click_search(self):
        try:
            self.utils.wait_for_element_clickable(self.SEARCH_BUTTON).click()
        except Exception as e:
            raise Exception(f"Error clicking search button: {e}")

    def get_hotel_data(self):
        try:
            self.utils.wait_for_element_visible(self.HOTEL_NAMES)
            hotels = self.driver.find_elements(*self.HOTEL_NAMES)
            tariffs = self.driver.find_elements(*self.HOTEL_TARIFFS)
            hotel_data = []
            for i in range(min(len(hotels), len(tariffs))):
                name = hotels[i].text.strip()
                price = tariffs[i].text.strip()
                if name and price:
                    hotel_data.append([name, price])
            return hotel_data
        except Exception as e:
            raise Exception(f"Error capturing hotel data: {e}")
