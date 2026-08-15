from django.contrib.auth.models import User
from django.db import models
import uuid


class Collection(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="collections"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CollectionMovie(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="movies"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    uuid = models.CharField(max_length=255)

    genres = models.TextField(blank=True)

    def __str__(self):
        return self.title