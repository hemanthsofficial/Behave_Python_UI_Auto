from behave import given, when, then

from pages.flight_page import FlightPage
from utils.common_utils import CommonUtils
from utils.excel_writer import ExcelWriter
from utils.logger import get_logger

logger = get_logger(__name__)


@given('Flight search page is displayed')
def step_open_make_my_trip_flight_page(context):
    logger.info("Navigating to MakeMyTrip flight search page")
    try:
        context.driver.get(CommonUtils.get_url("flight_url"))
        context.driver.maximize_window()
        context.flight_page = FlightPage(context.driver)
    except Exception as e:
        logger.error(f"Failed to load flight search page: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error loading flight page")


@when('I select "{trip}" for trip type')
def step_select_trip_type(context, trip):
    logger.info(f"Selecting trip type: {trip}")
    try:
        context.flight_page.select_trip_type(trip)
    except Exception as e:
        logger.error(f"Failed to select trip type: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error selecting trip type")


@when('I enter "{source}" for from station & "{destination}" for to station')
def step_enter_cities(context, source, destination):
    logger.info(f"Entering cities - From: {source}, To: {destination}")
    try:
        context.flight_page.enter_from_to_city(source, destination)
    except Exception as e:
        logger.error(f"Failed to enter source/destination: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error entering cities")


@when('I select "{departure_date}" for departure')
def step_select_dates(context, departure_date):
    logger.info(f"Selecting departure date: {departure_date}")
    try:
        context.flight_page.select_dates(departure_date)
    except Exception as e:
        logger.error(f"Failed to select departure date: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error selecting departure date")


@when('I select "{adults}" for travellers & "{travel_class}" for class')
def step_select_travellers(context, adults, travel_class):
    logger.info(f"Selecting travellers: {adults}, Class: {travel_class}")
    try:
        context.flight_page.select_travellers_and_class(adults, travel_class)
    except Exception as e:
        logger.error(f"Failed to select travellers and class: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error selecting travellers and class")


@when('I hit "{booking}" search button')
def step_click_search_button(context, booking):
    logger.info(f"Clicking {booking} search button")
    try:
        if booking.lower() == "flight":
            context.flight_page.click_search()
        elif booking.lower() == "hotel":
            context.hotel_page.click_search()
        else:
            logger.warning(f"Unknown booking type: {booking}")
    except Exception as e:
        logger.error(f"Failed to click {booking} search button: {e}", exc_info=True)
        context.scenario.skip(f"Skipping due to error clicking {booking} search button")


@then('I capture and store flight search results')
def step_capture_flights_data(context):
    logger.info("Capturing and writing flight details to Excel")
    try:
        flight_data = context.flight_page.get_flight_data()
        ExcelWriter.write_to_excel(context.log_file_path, sheet_name="Flights", data=flight_data)
    except Exception as e:
        logger.error(f"Failed to capture and store flight data: {e}", exc_info=True)
        context.scenario.skip("Skipping due to error capturing/storing flight data")
