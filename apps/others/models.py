from unittest.util import _MAX_LENGTH
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import Tag


class Item(models.Model):
    item = models.CharField(max_length=200)

    PRIORITY_CHOICES = [("---------", "---------"), ("!", "较低"), ("!!", "一般"), ("!!!", "较高")]

    priority = models.CharField(
        max_length=15, choices=PRIORITY_CHOICES, default="----"
    )

    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, blank=True, null=True)

    date = models.DateField(default=timezone.now, blank=True)

    period = models.CharField(max_length=200, blank=True)

    note = models.TextField(blank=True)

    class Meta:
        ordering = ["item", "priority", "tag"]

    def __str__(self):
        return f"{self.item} {self.priority} {self.tag}"

    def get_absolute_url(self):
        return reverse("item-detail", kwargs={"pk": self.pk})


