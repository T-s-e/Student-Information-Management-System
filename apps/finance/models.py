from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import AcademicSession, AcademicTerm, SubjectClass
from apps.subjects.models import Subject


class Invoice(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    class_for = models.ForeignKey(SubjectClass, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[("已完成", "已完成"), ("未完成", "未完成")],
        default="未完成",
    )

    class Meta:
        ordering = ["subject", "term"]

    def __str__(self):
        return f"{self.subject}"

    def get_absolute_url(self):
        return reverse("invoice-detail", kwargs={"pk": self.pk})


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    amount = models.CharField(max_length=2000)

