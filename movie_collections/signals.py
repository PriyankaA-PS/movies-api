from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Collection, CollectionMovie, CollectionActivityLog


@receiver(post_save, sender=Collection)
def log_collection_created(sender, instance, created, **kwargs):
    """
    Fires every time a Collection row is saved (INSERT or UPDATE).

    sender   -> the model class that sent the signal: Collection
    instance -> the actual Collection object that was just saved
    created  -> True on INSERT, False on UPDATE
    kwargs   -> anything else Django/DRF passes along (raw, using, update_fields...)

    This writes a real row to CollectionActivityLog, which is the whole
    point of the exercise: the view/serializer never mention "log an
    activity" anywhere — this side effect is attached to the model itself.
    """
    if created:
        CollectionActivityLog.objects.create(
            collection=instance,
            action=f"Collection '{instance.title}' created "
                   f"by '{instance.user.username}'",
        )
    else:
        CollectionActivityLog.objects.create(
            collection=instance,
            action=f"Collection '{instance.title}' updated",
        )


@receiver(post_save, sender=CollectionMovie)
def log_collection_movie_created(sender, instance, created, **kwargs):
    """
    The serializer's create() loops over movies_data and calls
    CollectionMovie.objects.create(...) once per movie, so this receiver
    fires once per movie in the POST payload — resulting in one
    CollectionActivityLog row per movie.
    """
    if created:
        CollectionActivityLog.objects.create(
            collection=instance.collection,
            action=f"Movie '{instance.title}' added to collection",
        )
