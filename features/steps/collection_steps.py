from behave import given, when, then


def collection_payload(title):
    return {
        "title": title,
        "description": "BDD test collection",
        "movies": [
            {
                "title": "Raiders of the Lost Ark",
                "description": "An archaeologist searches for the Ark.",
                "genres": "Action, Adventure",
                "uuid": "84",
            },
            {
                "title": "Test Movie",
                "description": "A test movie.",
                "genres": "Action, Thriller",
                "uuid": "85",
            },
        ],
    }


@when('I create a collection titled "{title}"')
@given('I create a collection titled "{title}"')
def step_create_collection(context, title):
    context.response = context.session.post(
        f"{context.base_url}/collection/",
        json=collection_payload(title),
    )
    # assert context.response.status_code == 200, (
    #     f"Expected 200 but received "
    #     f"{context.response.status_code}: "
    #     f"{context.response.text}"
    # )
    #
    data = context.response.json()

    if context.response.status_code == 200:
        context.collection_uuid = data["collection_uuid"]


@then("the collection response status should be 200")
def step_collection_status_201(context):
    assert context.response.status_code == 200, (
        f"Expected 200 but received "
        f"{context.response.status_code}: "
        f"{context.response.text}"
    )


@then("the collection response status should be 401")
def step_collection_status_401(context):
    assert context.response.status_code == 401


@then("the response should contain a collection UUID")
def step_collection_uuid(context):
    data = context.response.json()

    assert "collection_uuid" in data
    assert data["collection_uuid"]

    context.collection_uuid = data["collection_uuid"]


@when("I request my collections")
def step_request_collections(context):
    context.response = context.session.get(
        f"{context.base_url}/collection/"
    )


@then("the collection list response status should be 200")
def step_collection_list_status(context):
    assert context.response.status_code == 200


@then('I should see "{title}" in my collections')
def step_collection_exists_in_response(context, title):
    data = context.response.json()

    collections = data["data"]["collections"]

    titles = [
        collection["title"]
        for collection in collections
    ]

    assert title in titles


@then('my favourite genres should contain "{genre}"')
def step_favourite_genre(context, genre):
    data = context.response.json()

    favourite_genres = data["data"]["favourite_genres"]

    assert genre in favourite_genres


@when("I request the collection details")
def step_request_collection_details(context):
    context.response = context.session.get(
        f"{context.base_url}/collection/"
        f"{context.collection_uuid}/"
    )


@then("the collection detail response status should be 200")
def step_collection_detail_status_200(context):
    assert context.response.status_code == 200


@then('the collection title should be "{title}"')
def step_collection_title(context, title):
    data = context.response.json()

    assert data["title"] == title


@given("I remember the collection UUID")
def step_remember_collection_uuid(context):
    context.remembered_collection_uuid = (
        context.collection_uuid
    )


@when("I request the remembered collection")
def step_request_remembered_collection(context):
    context.response = context.session.get(
        f"{context.base_url}/collection/"
        f"{context.remembered_collection_uuid}/"
    )


@then("the collection detail response status should be 404")
def step_collection_detail_status_404(context):
    assert context.response.status_code == 404