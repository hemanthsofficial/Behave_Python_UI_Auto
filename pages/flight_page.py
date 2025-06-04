from selenium.webdriver.common.by import By
from utils.common_utils import CommonUtils


class FlightPage:
    def __init__(self, driver):
        self.driver = driver
        self.utils = CommonUtils(driver)

    # Locators
    FROM_INPUT = (By.ID, "fromCity")
    TO_INPUT = (By.ID, "toCity")
    CITY_INPUT = (By.XPATH, "//input[@placeholder='From']")
    CITY_RESULT = (By.XPATH, "//ul[@role='listbox']//li")
    DEPARTURE_DATE_BOX = (By.XPATH, "//label[@for='departure']")
    RETURN_DATE_BOX = (By.XPATH, "//label[@for='return']")
    ADULTS_DROPDOWN = (By.XPATH, "//span[text()='Travellers & Class']")
    SEARCH_BTN = (By.XPATH, "//a[text()='Search']")
    SEARCH_RESULT = (By.XPATH, "//span[@class='airlineInfo-sctn']//span")

    # actions
    def enter_from_to_city(self, source, destination):
        try:
            self.utils.wait_for_element_clickable(self.FROM_INPUT).click()
            self.utils.wait_for_element_visible(self.CITY_INPUT).send_keys(source)
            self.utils.wait_for_all_elements_visible(self.CITY_RESULT)[0].click()

            self.utils.wait_for_element_clickable(self.TO_INPUT).click()
            self.utils.wait_for_element_visible(self.CITY_INPUT).send_keys(destination)
            self.utils.wait_for_all_elements_visible(self.CITY_RESULT)[0].click()
        except Exception as e:
            raise Exception(f"Error entering origin '{origin}' or destination '{destination}': {e}")

    def select_dates(self, departure, return_date):
        try:
            self.utils.select_date(departure)
            self.utils.select_date(return_date)
        except Exception as e:
            raise Exception(f"Error selecting travel date '{date}': {e}")

    def select_travellers_and_class(self, adults, travel_class):
        try:
            self.utils.wait_for_element_clickable(self.ADULTS_DROPDOWN).click()
            # implement
        except Exception as e:
            raise Exception(f"Error selecting travellers/class '{date}': {e}")

    def click_search(self):
        try:
            self.utils.wait_for_element_clickable(self.SEARCH_BTN).click()
        except:
            raise Exception(f"Error clicking flight search button: {e}")

    def get_flight_names(self):
        try:
            elements = self.utils.wait_for_all_elements_visible(self.SEARCH_RESULT)
            return list(set([e.text.strip() for e in elements if e.text.strip()]))
        except:
            raise Exception(f"Error capturing flight data: {e}")
