from django.urls import path

from .views import (
    WorkCreateView,
    WorkDeleteView,
    WorkDetailView,
    WorkListView,
    WorkUpdateView,
)

urlpatterns = [
    path("list/", WorkListView.as_view(), name="work-list"),
    path("<int:pk>/", WorkDetailView.as_view(), name="work-detail"),
    path("create/", WorkCreateView.as_view(), name="work-create"),
    path("<int:pk>/update/", WorkUpdateView.as_view(), name="work-update"),
    path("<int:pk>/delete/", WorkDeleteView.as_view(), name="work-delete"),
]
