Feature: Search Hotels

  Scenario Outline: Capture hotel details
    Given hotel search page is displayed
    When I enter "<location>" for location
    And I select "<checkin>" for check-in and "<checkout>" for check-out
    And I select "<rooms>" for room and "<adults>" for adults
    And I hit "<type>" search button
    Then I capture and store hotel names and tariffs

    Examples:
    | location  | checkin     | checkout    | rooms  | adults  | type  |
    | Kochi     | 12-06-2025  | 14-06-2025  | 1      | 1       | hotel |