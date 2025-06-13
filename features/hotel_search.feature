Feature: Search Hotels

  Scenario Outline: Capture hotel details
    Given Hotel search page is displayed
    When I select "<room>" for room type
    And I enter "<location>" for location
    And I select "<checkin>" for check-in and "<checkout>" for check-out
    And I select "<rooms>" for room and "<adults>" for adults
    And I hit "<booking>" search button
    Then I capture and store hotel search results

    Examples:
    | room          | location  | checkin     | checkout    | rooms  | adults  | booking  |
    | Upto 4 rooms  | Cochin    | 15-06-2025  | 17-06-2025  | 01     | 01      | hotel    |