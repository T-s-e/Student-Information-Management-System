from unittest.util import _MAX_LENGTH
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import SubjectClass


class Subject(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    PROPERTY_CHOICES = [("compulsory", "必修"), ("optional", "选修")]


    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )
    credit = models.CharField(max_length=200, unique=True)
    subject = models.CharField(max_length=200)
    professor = models.CharField(max_length=200)
    # online_source = models.CharField(max_length=200, blank=True)
    online_source = models.URLField(max_length=200)
    property = models.CharField(max_length=10, choices=PROPERTY_CHOICES, default="必修")
    date_of_birth = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        SubjectClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_of_admission = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="subjects/passports/")

    class Meta:
        ordering = ["subject", "professor", "online_source"]

    def __str__(self):
        return f"{self.subject} {self.professor} {self.online_source} ({self.credit})"

    def get_absolute_url(self):
        return reverse("subject-detail", kwargs={"pk": self.pk})


class SubjectBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="subjects/bulkupload/")
