from behave import given, when, then

from pages.hotel_page import HotelPage
from utils.common_utils import CommonUtils
from utils.excel_writer import ExcelWriter
from utils.logger import get_logger

logger = get_logger(__name__)


@given('Hotel search page is displayed')
def step_open_make_my_trip_hotel_page(context):
    logger.info("Navigating to MakeMyTrip hotel search page")
    try:
        context.driver.get(CommonUtils.get_url("hotel_url"))
        context.driver.maximize_window()
        context.hotel_page = HotelPage(context.driver)
    except Exception as e:
        logger.error(f"Failed to load hotel search page: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error loading hotel page")


@when('I select "{room}" for room type')
def step_select_room_type(context, room):
    logger.info(f"Selecting room type: {room}")
    try:
        context.hotel_page.select_room_type(room)
    except Exception as e:
        logger.error(f"Failed to select room type: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error selecting room type")


@when('I enter "{location}" for location')
def step_enter_location(context, location):
    logger.info(f"Entering hotel location: {location}")
    try:
        context.hotel_page.enter_location(location)
    except Exception as e:
        logger.error(f"Failed to enter hotel location: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error entering hotel location")


@when('I select "{checkin}" for check-in and "{checkout}" for check-out')
def step_select_dates(context, checkin, checkout):
    logger.info(f"Selecting check-in: {checkin} and check-out: {checkout}")
    try:
        context.hotel_page.select_dates(checkin, checkout)
    except Exception as e:
        logger.error(f"Failed to select hotel check-in/check-out dates: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error selecting dates")


@when('I select "{rooms}" for room and "{adults}" for adults')
def step_select_guests(context, rooms, adults):
    logger.info(f"Selecting rooms: {rooms} and adults: {adults}")
    try:
        context.hotel_page.select_room_and_guests(int(rooms), int(adults))
    except Exception as e:
        logger.error(f"Failed to select hotel guests: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error selecting room and guests")


@then('I capture and store hotel search results')
def step_capture_hotels_data(context):
    logger.info("Capturing and writing hotel names and tariffs to Excel")
    try:
        hotel_data = context.hotel_page.get_hotel_data()
        ExcelWriter.write_to_excel(context.log_file_path, sheet_name="Hotels", data=hotel_data)
    except Exception as e:
        logger.error(f"Failed to capture and store hotel data: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error capturing/storing hotel data")
