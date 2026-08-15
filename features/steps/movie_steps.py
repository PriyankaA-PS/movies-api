import requests

from behave import given, when, then


@when("I request the movie list")
def step_request_movie_list(context):
    context.response = context.session.get(
        f"{context.base_url}/movies/"
    )


@then("the movie response status should be 200")
def step_movie_status_200(context):
    assert context.response.status_code == 200


@then("the movie response status should be 401")
def step_movie_status_401(context):
    assert context.response.status_code == 401


@then("the movie response should contain movies")
def step_movie_response_contains_movies(context):
    data = context.response.json()

    assert isinstance(data, list)

    if data:
        assert "title" in data[0]


@when("the movie service is unavailable")
def step_movie_service_unavailable(context):
    """
    This scenario cannot mock the Django process from Behave
    when Behave is running as a separate process.

    Keep external-service failure testing in your unit tests
    using mock.patch(), or introduce a dedicated mock server.
    """
    raise NotImplementedError(
        "Use unit tests for external API failure scenarios."
    )


@then("the movie response status should be 503")
def step_movie_status_503(context):
    assert context.response.status_code == 503