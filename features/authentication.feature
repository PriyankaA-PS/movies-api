Feature: User authentication

  Scenario: User can register successfully
    Given I am not authenticated
    When I register with username "bdd_register_user" and password "TestPassword123"
    Then the registration response status should be 201
    And the response should contain an access token

  Scenario: User cannot register with duplicate username
    Given I have registered as "bdd_duplicate_user" with password "TestPassword123"
    When I register with username "bdd_duplicate_user" and password "TestPassword123"
    Then the registration response status should be 400

  Scenario: User can login successfully
    Given I have registered as "bdd_login_user" with password "TestPassword123"
    When I login with username "bdd_login_user" and password "TestPassword123"
    Then the login response status should be 200
    And the login response should contain an access token
    And the login response should contain a refresh token

  Scenario: User cannot login with invalid password
    Given I have registered as "bdd_invalid_login" with password "TestPassword123"
    When I login with username "bdd_invalid_login" and password "WrongPassword123"
    Then the login response status should be 401

  Scenario: Authenticated user can logout
    Given I have registered as "bdd_logout_user" with password "TestPassword123"
    And I login as "bdd_logout_user" with password "TestPassword123"
    When I logout
    Then the logout response status should be 200
    And the logout response message should be "Logout successful"

  Scenario: Unauthenticated user cannot logout
    Given I am not authenticated
    When I logout without authentication
    Then the logout response status should be 401