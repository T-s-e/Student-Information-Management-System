from django.urls import path

from .views import (
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemListView,
    ItemUpdateView,
)

urlpatterns = [
    path("list", ItemListView.as_view(), name="item-list"),
    path("<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("create/", ItemCreateView.as_view(), name="item-create"),
    path("<int:pk>/update/", ItemUpdateView.as_view(), name="item-update"),
    path("delete/<int:pk>/", ItemDeleteView.as_view(), name="item-delete"),
]
