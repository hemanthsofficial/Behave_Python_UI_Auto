from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.logger import get_logger
logger = get_logger(__name__)


class DriverFactory:
    @staticmethod
    def get_driver():
        logger.info("Initializing WebDriver")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(10)
        logger.info("WebDriver initialized successfully")
        return driver
