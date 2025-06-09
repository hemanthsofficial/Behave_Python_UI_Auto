Feature: Search Flights

  Scenario Outline: Capture all flights from City A to City B
    Given MakeMyTrip homepage is displayed
    When I select "<trip>" for trip type
    And I enter "<source>" for from station & "<destination>" for to station
    And I select "<departure_date>" for departure
    And I select "<adults>" for travellers & "<travel_class>" for class
    And I hit "<type>" search button
    Then I capture and store flight names

    Examples:
    | trip    | source  | destination | departure_date | adults  | travel_class  | type    |
    | One Way | Chennai | Kochi       | 12-06-2025     | 1       | business      | flight  |
