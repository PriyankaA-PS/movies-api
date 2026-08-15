import requests

from behave import given, when, then


@given("I am not authenticated")
def step_not_authenticated(context):
    context.session = requests.Session()


@given(
    'I have registered as "{username}" with password "{password}"'
)
def step_register_user(context, username, password):
    context.session = requests.Session()

    response = context.session.post(
        f"{context.base_url}/register/",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 201, (
        f"Registration failed: "
        f"{response.status_code} {response.text}"
    )


@when(
    'I register with username "{username}" and password "{password}"'
)
def step_register(context, username, password):
    context.response = context.session.post(
        f"{context.base_url}/register/",
        json={
            "username": username,
            "password": password,
        },
    )


@then("the registration response status should be 201")
def step_registration_status_201(context):
    assert context.response.status_code == 201


@then("the registration response status should be 400")
def step_registration_status_400(context):
    assert context.response.status_code == 400


@then("the response should contain an access token")
def step_access_token(context):
    data = context.response.json()

    assert "access_token" in data
    assert data["access_token"]


@when(
    'I login with username "{username}" and password "{password}"'
)
def step_login(context, username, password):
    context.response = context.session.post(
        f"{context.base_url}/login/",
        json={
            "username": username,
            "password": password,
        },
    )


@then("the login response status should be 200")
def step_login_status_200(context):
    assert context.response.status_code == 200


@then("the login response status should be 401")
def step_login_status_401(context):
    assert context.response.status_code == 401


@then("the login response should contain an access token")
def step_login_access_token(context):
    data = context.response.json()

    assert "access" in data
    assert data["access"]


@then("the login response should contain a refresh token")
def step_login_refresh_token(context):
    data = context.response.json()

    assert "refresh" in data
    assert data["refresh"]


@given(
    'I login as "{username}" with password "{password}"'
)
def step_login_authenticated(context, username, password):
    context.response = context.session.post(
        f"{context.base_url}/login/",
        json={
            "username": username,
            "password": password,
        },
    )

    assert context.response.status_code == 200

    data = context.response.json()

    context.access_token = data["access"]
    context.refresh_token = data["refresh"]

    context.session.headers.update(
        {
            "Authorization": f"Bearer {context.access_token}"
        }
    )


@when("I logout")
def step_logout(context):
    context.response = context.session.post(
        f"{context.base_url}/logout/",
        json={
            "refresh": context.refresh_token
        },
    )


@then("the logout response status should be 200")
def step_logout_status_200(context):
    assert context.response.status_code == 200


@then('the logout response message should be "Logout successful"')
def step_logout_message(context):
    data = context.response.json()

    assert data["message"] == "Logout successful"


@when("I logout without authentication")
def step_logout_without_authentication(context):
    context.response = context.session.post(
        f"{context.base_url}/logout/",
        json={
            "refresh": "invalid-refresh-token"
        },
    )


@then("the logout response status should be 401")
def step_logout_status_401(context):
    assert context.response.status_code == 401