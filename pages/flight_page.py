from selenium.webdriver.common.by import By
from utils.common_utils import CommonUtils


class FlightPage:
    def __init__(self, driver):
        self.driver = driver
        self.utils = CommonUtils(driver)

    # Locators
    section = "FLIGHT_PAGE"
    FROM_INPUT = (By.ID, CommonUtils.get_locator(section, "from_input"))
    TO_INPUT = (By.ID, CommonUtils.get_locator(section, "to_input"))
    CITY_INPUT = (By.XPATH, CommonUtils.get_locator(section, "city_input"))
    CITY_RESULT = (By.XPATH, CommonUtils.get_locator(section, "city_result"))
    DEPARTURE_DATE_BOX = (By.ID, CommonUtils.get_locator(section, "departure_date_box"))
    RETURN_DATE_BOX = (By.ID, CommonUtils.get_locator(section, "return_date_box"))
    ADULTS_DROPDOWN = (By.ID, CommonUtils.get_locator(section, "adults_dropdown"))
    ADULTS_BTN = (By.XPATH, CommonUtils.get_locator(section, "adults_btn"))
    CLASS_BTN = (By.XPATH, CommonUtils.get_locator(section, "class_btn"))
    APPLY_BTN = (By.XPATH, CommonUtils.get_locator(section, "apply_btn"))
    SEARCH_BTN = (By.XPATH, CommonUtils.get_locator(section, "search_btn"))
    SEARCH_RESULT = (By.XPATH, CommonUtils.get_locator(section, "search_result"))

    # actions
    def enter_from_to_city(self, source, destination):
        try:
            self.utils.wait_for_element_clickable(self.FROM_INPUT).click()
            self.utils.wait_for_element_visible(self.FROM_INPUT).send_keys(source)
            self.utils.wait_for_all_elements_visible(self.CITY_RESULT)[0].click()

            self.utils.wait_for_element_clickable(self.TO_INPUT).click()
            self.utils.wait_for_element_visible(self.TO_INPUT).send_keys(destination)
            self.utils.wait_for_all_elements_visible(self.CITY_RESULT)[0].click()
        except Exception as e:
            raise Exception(f"Error entering source('{source}')/destination('{destination}'): {e}")

    def select_dates(self, departure_date, return_date):
        try:
            self.utils.select_date(departure_date)
            self.utils.select_date(return_date)
        except Exception as e:
            raise Exception(f"Error selecting departure('{departure_date}')/return('{return_date}') date: {e}")

    def select_travellers_and_class(self, adults, travel_class):
        try:
            self.utils.wait_for_element_clickable(self.ADULTS_DROPDOWN).click()
            self.utils.wait_for_all_elements_visible(self.ADULTS_BTN)[1].click()
            self.utils.wait_for_all_elements_visible(self.CLASS_BTN)[3].click()
            self.utils.wait_for_element_visible(self.APPLY_BTN).click()
        except Exception as e:
            raise Exception(f"Error selecting travellers('{adults}')/class('{travel_class}'): {e}")

    def click_search(self):
        try:
            self.utils.wait_for_element_clickable(self.SEARCH_BTN).click()
        except Exception as e:
            raise Exception(f"Error clicking flight search button: {e}")

    def get_flight_names(self):
        try:
            elements = self.utils.wait_for_all_elements_visible(self.SEARCH_RESULT)
            return list(set([e.text.strip() for e in elements if e.text.strip()]))
        except Exception as e:
            raise Exception(f"Error capturing flight data: {e}")
