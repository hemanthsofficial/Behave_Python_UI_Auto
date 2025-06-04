from selenium.webdriver.common.by import By

from utils.common_utils import CommonUtils


class HotelPage:
    def __init__(self, driver):
        self.driver = driver
        self.utils = CommonUtils(driver)

    # Locators
    LOCATION_INPUT_BOX = (By.XPATH, "//input[@placeholder='Enter city/ Hotel/ Area/ Building']")
    FIRST_SUGGESTION = (By.XPATH, "//ul[@role='listbox']//li")
    SEARCH_BUTTON = (By.XPATH, "//button[text()='Search']")
    HOTEL_NAMES = (By.XPATH, "//p[@itemprop='name']")
    HOTEL_TARIFFS = (By.XPATH, "//span[contains(@class,'actualPrice')]")

    # Actions
    def enter_location(self, location):
        try:
            self.utils.wait_for_element_clickable(self.LOCATION_INPUT_BOX).click()
            input_box = self.utils.wait_for_element_visible(self.LOCATION_INPUT_BOX)
            input_box.send_keys(location)
            self.utils.wait_for_element_clickable(self.FIRST_SUGGESTION).click()
        except Exception as e:
            raise Exception(f"Error entering location '{location}': {e}")

    def select_dates(self, checkin, checkout):
        try:
            # Click check-in
            checkin_element = self.driver.find_element(By.XPATH, f"//div[@aria-label='{checkin}']")
            checkin_element.click()

            # Click check-out
            checkout_element = self.driver.find_element(By.XPATH, f"//div[@aria-label='{checkout}']")
            checkout_element.click()
        except Exception as e:
            raise Exception(f"Error selecting dates ({checkin} to {checkout}): {e}")

    def select_room_and_guests(self, rooms, adults):
        try:
            #need to implement
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
