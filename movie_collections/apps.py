from django.apps import AppConfig


class MovieCollectionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie_collections'

    def ready(self):
        # Importing the module registers its @receiver-decorated functions
        # with Django's signal dispatcher. This must happen once, after the
        # app registry is fully loaded — ready() is the correct hook for that.
        import movie_collections.signals  # noqa: F401
