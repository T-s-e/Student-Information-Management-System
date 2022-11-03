from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    Tag,
    Course,
)
from apps.subjects.models import Subject

from .utils import score_grade


# Create your models here.
class Result(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    current_class = models.ForeignKey(Tag, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    test_score = models.IntegerField(default=0)
    exam_score = models.IntegerField(default=0)

    class Meta:
        ordering = ["course"]

    def __str__(self):
        return f"{self.subject} {self.session} {self.term} {self.course}"

    def total_score(self):
        return self.test_score + self.exam_score

    def grade(self):
        return score_grade(self.total_score())
