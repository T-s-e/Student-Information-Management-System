from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Work(models.Model):
    STATUS = [("private", "个人"), ("collaboration", "协作")]

    PRIORITY = [("!", "较低"), ("!!", "一般"), ("!!!", "较高")]

    current_method = models.CharField(max_length=15, choices=STATUS, default="private")
    name = models.CharField(max_length=200)
    period = models.CharField(max_length=200, default="None")
    # other_name = models.CharField(max_length=200, blank=True)
    priority = models.CharField(max_length=15, choices=PRIORITY, default="!")
    # date_of_birth = models.DateField(default=timezone.now)
    # date = models.DateField(default=timezone.now, blank=True)

    note = models.TextField(blank=True)

    # address = models.TextField(blank=True)
    # others = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("work-detail", kwargs={"pk": self.pk})
