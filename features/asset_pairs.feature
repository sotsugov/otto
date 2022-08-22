@public_api
Feature: Public API Trading Pairs
  Get tradable asset pairs

  Scenario Outline: Retrieves XBT/USD trading pair
    Given I query public API "AssetPairs" endpoint
    And I request the "<pair>" asset pair
    When I make a request
    Then the response is successful
    And the response does not contain errors
    And the response result length is "<length>"
    And the response result contains "<pair>"

    Examples:
      | pair                   | length |
      | XXBTZUSD               | 1      |
      | ADAEUR                 | 1      |
      | DAIUSD                 | 1      |
      | XTZGBP                 | 1      |
      | XXBTZUSD,YGGEUR        | 2      |
      | ADAEUR,YGGEUR,1INCHEUR | 3      |

