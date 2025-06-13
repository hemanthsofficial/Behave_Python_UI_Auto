Feature: Search Flights

  Scenario Outline: Capture all flights from City A to City B
    Given Flight search page is displayed
    When I select "<trip>" for trip type
    And I enter "<source>" for from station & "<destination>" for to station
    And I select "<departure_date>" for departure
    And I select "<adults>" for travellers & "<travel_class>" for class
    And I hit "<booking>" search button
    Then I capture and store flight search results

    Examples:
    | trip    | source  | destination | departure_date | adults  | travel_class            | booking |
    | One Way | Chennai | Kochi       | 15-06-2025     | 1       | Economy/Premium Economy | flight  |
