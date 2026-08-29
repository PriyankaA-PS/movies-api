from django.urls import path

from .views import (
    CollectionView,
    CollectionDetailsView,
    CollectionReportView,
    TaskStatusView,
)

urlpatterns = [
    path("collection/", CollectionView.as_view(), name="collection"),
    path("collection/<uuid:collection_uuid>/",CollectionDetailsView.as_view(), name="collection-detail",),
    path("collection/<uuid:collection_uuid>/report/", CollectionReportView.as_view(), name="collection-report"),
    path("tasks/<str:task_id>/", TaskStatusView.as_view(), name="task-status"),
]