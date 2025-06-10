import os
import time
from datetime import datetime

import allure
from allure_commons.types import AttachmentType

from utils.common_utils import CommonUtils
from utils.driver_factory import DriverFactory
from utils.logger import get_logger


def before_all(context):
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    context.logger = get_logger('BehaveRun', log_file=log_file)
    context.log_file_path = log_file
    context.logger.info("=== Test Run Started ===")
    context.driver = DriverFactory.get_driver()


def after_all(context):
    context.logger.info("=== Test Run Finished ===")
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()


def before_scenario(context, scenario):
    context.logger.info(f"--- Scenario Started: {scenario.name} ---")
    allure.dynamic.title(scenario.name)


def after_scenario(context, scenario):
    context.logger.info(f"--- Scenario Finished: {scenario.name} ---")


def after_step(context, step):
    if step.status == "failed":
        context.logger.error(f"Step failed: {step.name}")

        if hasattr(context, 'driver'):
            utils = CommonUtils(context.driver)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/failed_step_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            utils.take_screenshot(screenshot_path)

            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name="Failure Screenshot", attachment_type=AttachmentType.PNG)

        try:
            if hasattr(context, 'log_file_path') and os.path.exists(context.log_file_path):
                with open(context.log_file_path, "r") as log_file:
                    allure.attach(log_file.read(), name="Execution Logs", attachment_type=AttachmentType.TEXT)
        except Exception as e:
            context.logger.warning(f"Could not attach log file to Allure: {e}")
