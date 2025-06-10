from behave import given, when, then
from pages.hotel_page import HotelPage
from utils.common_utils import CommonUtils
from utils.excel_writer import ExcelWriter
from utils.logger import get_logger

logger = get_logger(__name__)


@given('hotel search page is displayed')
def step_open_make_my_trip_hotel_page(context):
    try:
        logger.info("Navigating to MakeMyTrip hotel search page")
        context.driver.get(CommonUtils.get_url("hotel_url"))
        context.driver.maximize_window()
        context.hotel_page = HotelPage(context.driver)
    except Exception as e:
        logger.error(f"Failed to load hotel search page: {e}", exc_info=True)
        assert False, f"Failed to load hotel search page: {e}"


@when('I enter "{location}" for location')
def step_enter_location(context, location):
    logger.info(f"Entering hotel location: {location}")
    try:
        context.hotel_page.enter_location(location)
    except Exception as e:
        logger.error(f"Failed to enter hotel location: {e}", exc_info=True)
        assert False, f"Failed to enter hotel location: {e}"


@when('I select "{checkin}" for check-in and "{checkout}" for check-out')
def step_select_dates(context, checkin, checkout):
    logger.info(f"Selecting check-in: {checkin} and check-out: {checkout}")
    try:
        context.hotel_page.select_dates(checkin, checkout)
    except Exception as e:
        logger.error(f"Failed to select hotel checkin/checkout dates: {e}", exc_info=True)
        assert False, f"Failed to select hotel checkin/checkout dates: {e}"


@when('I select "{rooms}" for room and "{adults}" for adults')
def step_select_guests(context, rooms, adults):
    logger.info(f"Selecting {rooms} room(s) and {adults} adult(s)")
    try:
        context.hotel_page.select_room_and_guests(int(rooms), int(adults))
    except Exception as e:
        logger.error(f"Failed to select hotel guests: {e}", exc_info=True)
        assert False, f"Failed to select hotel guests: {e}"


@then('I capture and store hotel names and tariffs')
def step_capture_hotels_data(context):
    logger.info("Capturing and writing hotel names and tariffs to Excel")
    try:
        hotel_data = context.hotel_page.get_hotel_data()
        logger.info(f"Captured hotel data: {hotel_data}")
        ExcelWriter.write_to_excel(sheet_name="Hotels", data=[["Hotel Name", "Tariff"]] + hotel_data)
    except Exception as e:
        logger.error(f"Failed to capture and store hotel data: {e}", exc_info=True)
        assert False, f"Failed to capture and store hotel data: {e}"
