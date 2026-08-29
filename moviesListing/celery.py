import os

from celery import Celery

# Tell Celery where Django's settings live before anything else touches
# Django, same as manage.py does.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moviesListing.settings")

app = Celery("moviesListing")

# Every setting whose name starts with CELERY_ in settings.py is picked up
# here (namespace="CELERY" strips that prefix), so broker URL, result
# backend, serializers etc. are configured in one familiar place instead of
# a separate celeryconfig.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Look for a tasks.py inside every app listed in INSTALLED_APPS and
# register whatever it finds there — this is why movie_collections/tasks.py
# doesn't need to be imported/registered anywhere by hand.
app.autodiscover_tasks()
