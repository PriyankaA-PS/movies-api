Feature: Movie listing

  Scenario: Authenticated user can get movies
    Given I have registered as "bdd_movie_user" with password "TestPassword123"
    And I login as "bdd_movie_user" with password "TestPassword123"
    When I request the movie list
    Then the movie response status should be 200
    And the movie response should contain movies

  Scenario: Unauthenticated user cannot get movies
    Given I am not authenticated
    When I request the movie list
    Then the movie response status should be 401

