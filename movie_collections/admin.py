from django.contrib import admin

from .models import Collection, CollectionMovie, CollectionActivityLog

admin.site.register(Collection)
admin.site.register(CollectionMovie)
admin.site.register(CollectionActivityLog)
