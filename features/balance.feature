@private_api
Feature: Private API Account Balance
  Retrieve all cash balances, net of pending withdrawals

  Scenario: Retrieves the account balance of the user
    Given I query private API "Balance" endpoint
    And I am an authenticated user
    When I make a request
    Then the response is successful
    And the response does not contain errors
    And the account balance is "GBP.HOLD" value "0.0000"
