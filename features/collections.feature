Feature: Movie collections

  Scenario: Authenticated user can create a collection
    Given I have registered as "bdd_collection_user" with password "TestPassword123"
    And I login as "bdd_collection_user" with password "TestPassword123"
    When I create a collection titled "Action Movies"
    Then the collection response status should be 200
    And the response should contain a collection UUID

  Scenario: Unauthenticated user cannot create a collection
    Given I am not authenticated
    When I create a collection titled "Unauthorized Collection"
    Then the collection response status should be 401

  Scenario: User can view their collections
    Given I have registered as "bdd_view_user" with password "TestPassword123"
    And I login as "bdd_view_user" with password "TestPassword123"
    And I create a collection titled "My Action Movies"
    When I request my collections
    Then the collection list response status should be 200
    And I should see "My Action Movies" in my collections

  Scenario: User can see their favourite genres
    Given I have registered as "bdd_genre_user" with password "TestPassword123"
    And I login as "bdd_genre_user" with password "TestPassword123"
    And I create a collection titled "Action Collection"
    When I request my collections
    Then the collection list response status should be 200
    And my favourite genres should contain "Action"

  Scenario: User can view collection details
    Given I have registered as "bdd_detail_user" with password "TestPassword123"
    And I login as "bdd_detail_user" with password "TestPassword123"
    And I create a collection titled "Detail Collection"
    When I request the collection details
    Then the collection detail response status should be 200
    And the collection title should be "Detail Collection"

  Scenario: User cannot access another user's collection
    Given I have registered as "bdd_owner" with password "TestPassword123"
    And I login as "bdd_owner" with password "TestPassword123"
    And I create a collection titled "Private Collection"
    And I remember the collection UUID
    And I have registered as "bdd_attacker" with password "TestPassword123"
    And I login as "bdd_attacker" with password "TestPassword123"
    When I request the remembered collection
    Then the collection detail response status should be 404