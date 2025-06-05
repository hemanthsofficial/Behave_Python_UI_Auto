from behave import given, when, then
from pages.hotel_page import HotelPage
from utils.common_utils import CommonUtils
from utils.excel_writer import ExcelWriter


@given('hotel search page is displayed')
def step_open_hotel_page(context):
    try:
        context.driver.get(CommonUtils.get_url("hotel_url"))
        context.driver.maximize_window()
        context.hotel_page = HotelPage(context.driver)
    except Exception as e:
        assert False, f"Failed to load hotel search page: {e}"


@when('I enter "{location}" for location')
def step_enter_hotel_location(context, location):
    try:
        context.hotel_page.enter_location(location)
    except Exception as e:
        assert False, f"Failed to enter hotel location: {e}"


@when('I select "{checkin}" for check-in and "{checkout}" for check-out')
def step_select_hotel_dates(context, checkin, checkout):
    try:
        context.hotel_page.select_dates(checkin, checkout)
    except Exception as e:
        assert False, f"Failed to select hotel checkin/checkout dates: {e}"


@when('I select "{rooms}" for room and "{adults}" for adults')
def step_select_guests(context, rooms, adults):
    try:
        context.hotel_page.select_guests(rooms, adults)
    except Exception as e:
        assert False, f"Failed to select hotel guests: {e}"


# reuse from flight_steps.py
# @when('I hit "{type}" search button')

@then('I capture and store hotel names and tariffs')
def step_capture_hotel_data(context):
    try:
        hotel_data = context.hotel_page.get_hotel_data()
        print("Hotels and Tariffs:")
        for row in hotel_data:
            print(row)
        ExcelWriter.write_to_excel(sheet_name="Hotels", data=[["Hotel Name", "Tariff"]] + hotel_data)
    except Exception as e:
        assert False, f"Failed to capture and store hotel data: {e}"
