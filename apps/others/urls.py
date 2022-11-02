from django.urls import path

from .views import (
    DownloadCSVViewdownloadcsv,
    OtherBulkUploadView,
    OtherCreateView,
    OtherDeleteView,
    OtherDetailView,
    OtherListView,
    OtherUpdateView,
)

urlpatterns = [
    path("list", OtherListView.as_view(), name="other-list"),
    path("<int:pk>/", OtherDetailView.as_view(), name="other-detail"),
    path("create/", OtherCreateView.as_view(), name="other-create"),
    path("<int:pk>/update/", OtherUpdateView.as_view(), name="other-update"),
    path("delete/<int:pk>/", OtherDeleteView.as_view(), name="other-delete"),
    path("upload/", OtherBulkUploadView.as_view(), name="other-upload"),
    path("download-csv/", DownloadCSVViewdownloadcsv.as_view(), name="download-csv"),
]
