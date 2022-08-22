@public_api
Feature: Public API Server Time
Get the server's time

  Scenario: Retrieves the server time
    Given I query public API "Time" endpoint
    When I make a request
    Then the response is successful
    And the response does not contain errors
    And latency is less than "10" ms
