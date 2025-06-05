from selenium import webdriver
from utils.driver_factory import DriverFactory


def before_all(context):
    context.driver = DriverFactory.get_driver()


def after_all(context):
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()
