import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CommonUtils:
    def __init__(self, driver):
        self.remote_driver = driver
        self.wait = WebDriverWait(driver, 10)

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

    # Select a date in the MakeMyTrip calendar widget
    def select_date(self, date_str):
        day, month, year = map(int, date_str.split("-"))
        month_year_to_select = datetime.date(year, month, day).strftime("%B %Y")

        while True:
            try:
                calendar_header = self.remote_driver.find_element(By.XPATH, "//div[@class='DayPicker-Caption']/div")
                if calendar_header.text.strip() == month_year_to_select:
                    date_xpath = f"//div[@class='DayPicker-Month'][.//div[text()='{month_year_to_select}']]//p[text()='{day}']"
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, date_xpath))).click()
                    break
                else:
                    # Click next month button
                    self.remote_driver.find_element(By.XPATH, "//span[@aria-label='Next Month']").click()
            except Exception as e:
                raise Exception(f"Failed to select date {date_str}: {e}")

    # Select passengers and travel class
    def select_passengers_and_class(self, adults, travel_class):
        # Click on adult count increment (assumes default is 1)
        for _ in range(int(adults) - 1):
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//li[@data-cy='adults-2'] | //li[contains(text(),'adults')]"))).click()

        # Select class
        class_xpath = f"//li[contains(text(),'{travel_class.title()}')]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, class_xpath))).click()

        # Click apply
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='APPLY']"))).click()
