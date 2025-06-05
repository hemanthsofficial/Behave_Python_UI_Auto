Feature: Search Hotels

  Scenario: Capture hotel details
    Given hotel search page is displayed
    When I enter "Kochi" for location
    And I select "03-06-2025" for check-in and "04-06-2025" for check-out
    And I select "1" for room and "1" for adults
    And I hit "hotel" search button
    Then I capture and store hotel names and tariffs
