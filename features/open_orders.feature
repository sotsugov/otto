@private_api
Feature: Private API Open Orders
  Retrieve information about currently open orders

  Scenario: Retrieves open orders for an account
    Given I query private API "OpenOrders" endpoint
    And I am an authenticated user
    When I make a request
    Then the response is successful
    And the response does not contain errors
    And ensures there are exactly "0" open orders
