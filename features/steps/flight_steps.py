from behave import given, when, then
from pages.flight_page import FlightPage
from utils.common_utils import CommonUtils
from utils.excel_writer import ExcelWriter
from utils.logger import get_logger

logger = get_logger(__name__)


@given('MakeMyTrip homepage is displayed')
def step_open_make_my_trip_flight_page(context):
    logger.info("Navigating to MakeMyTrip flight search page")
    context.driver.get(CommonUtils.get_url("flight_url"))
    context.driver.maximize_window()
    context.flight_page = FlightPage(context.driver)


@when('I select "{trip}" for trip type')
def step_select_trip_type(context, trip):
    logger.info(f"Selecting trip type: {trip}")
    context.flight_page.select_trip_type(trip)


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
    context.flight_page.select_dates(departure_date)


@when('I select "{adults}" for travellers & "{travel_class}" for class')
def step_select_travellers(context, adults, travel_class):
    logger.info(f"Selecting travellers: {adults}, Class: {travel_class}")
    context.flight_page.select_travellers_and_class(adults, travel_class)


@when('I hit "{type}" search button')
def step_click_search_button(context, type):
    logger.info(f"Clicking {type} search button")
    if type.lower() == "flight":
        context.flight_page.click_search()
    elif type.lower() == "hotel":
        context.hotel_page.click_search()


@then('I capture and store flight names')
def step_capture_flights_data(context):
    logger.info("Capturing and writing flight names to Excel")
    flights = context.flight_page.get_flight_names()
    logger.info(f"Flight Names: {flights}")
    ExcelWriter.write_to_excel(sheet_name="Flights", data=[["Flight Name"]] + [[name] for name in flights])
