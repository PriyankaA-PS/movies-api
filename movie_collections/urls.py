from django.urls import path

from .views import CollectionView, CollectionDetailsView

urlpatterns = [
    path("collection/", CollectionView.as_view(), name="collection"),
    path("collection/<uuid:collection_uuid>/",CollectionDetailsView.as_view(), name="collection-detail",)
]