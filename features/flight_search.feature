Feature: Search Flights

  Scenario: Capture all flights from City A to City B
    Given MakeMyTrip homepage is displayed
    When I enter "Chennai" for from station & "Kochi" for to station
    And I select "03-06-2025" for departure & "04-06-2025" for return
    And I select "1" for travellers & "business" for class
    And I hit "flight" search button
    Then I capture and store flight names
