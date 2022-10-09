from django.urls import path

from .views import (
    DownloadCSVViewdownloadcsv,
    SubjectBulkUploadView,
    SubjectCreateView,
    SubjectDeleteView,
    SubjectDetailView,
    SubjectListView,
    SubjectUpdateView,
)

urlpatterns = [
    path("list", SubjectListView.as_view(), name="subject-list"),
    path("<int:pk>/", SubjectDetailView.as_view(), name="subject-detail"),
    path("create/", SubjectCreateView.as_view(), name="subject-create"),
    path("<int:pk>/update/", SubjectUpdateView.as_view(), name="subject-update"),
    path("delete/<int:pk>/", SubjectDeleteView.as_view(), name="subject-delete"),
    path("upload/", SubjectBulkUploadView.as_view(), name="subject-upload"),
    path("download-csv/", DownloadCSVViewdownloadcsv.as_view(), name="download-csv"),
]
