import os

# BASE_URL = "http://127.0.0.1:8000"
BASE_URL = "http://localhost:9000"


def before_all(context):
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "moviesListing.settings"
    )

    import django
    django.setup()

    context.base_url = BASE_URL


def before_scenario(context, scenario):
    context.created_users = set()
    context.created_collections = set()


def after_scenario(context, scenario):
    from django.contrib.auth.models import User
    from movie_collections.models import Collection

    # Find all users created by Behave
    bdd_users = User.objects.filter(
        username__startswith="bdd_"
    )

    # Delete their collections first
    Collection.objects.filter(
        user__in=bdd_users
    ).delete()

    # Delete the BDD users
    bdd_users.delete()