from behave import given, when, then
from pages.flight_page import FlightPage
from utils.common_utils import CommonUtils
from utils.excel_writer import ExcelWriter


@given('MakeMyTrip homepage is displayed')
def step_open_make_my_trip(context):
    try:
        context.driver.get(CommonUtils.get_url("flight_url"))
        context.driver.maximize_window()
        context.flight_page = FlightPage(context.driver)
    except Exception as e:
        assert False, f"Failed to load flight search page: {e}"


@when('I enter "{source}" for from station & "{destination}" for to station')
def step_enter_cities(context, source, destination):
    try:
        context.flight_page.enter_from_to_city(source, destination)
    except Exception as e:
        assert False, f"Failed to enter source/destination: {e}"


@when('I select "{departure_date}" for departure & "{return_date}" for return')
def step_select_dates(context, departure_date, return_date):
    try:
        context.flight_page.select_dates(departure_date, return_date)
    except Exception as e:
        assert False, f"Failed to select departure/return date: {e}"


@when('I select "{adults}" for travellers & "{travel_class}" for class')
def step_select_travellers(context, adults, travel_class):
    try:
        context.flight_page.select_travellers_and_class(adults, travel_class)
    except Exception as e:
        assert False, f"Failed to select travellers & class: {e}"


@when('I hit "{type}" search button')
def step_click_search_button(context, type):
    try:
        if type.lower() == "flight":
            context.flight_page.click_search()
        elif type.lower() == "hotel":
            context.hotel_page.click_search()
    except Exception as e:
        assert False, f"Failed to hit search button: {e}"


@then('I capture and store flight names')
def step_capture_flights(context):
    try:
        flights = context.flight_page.get_flight_names()
        print("Flight Names:", flights)
        ExcelWriter.write_to_excel(sheet_name="Flights", data=[["Flight Name"]] + [[name] for name in flights])
    except Exception as e:
        assert False, f"Failed to capture and store flight data: {e}"
