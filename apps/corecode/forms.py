from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    Tag,
    Course,
)

SiteConfigForm = modelformset_factory(
    SiteConfig,
    fields=(
        "key",
        "value",
    ),
    extra=0,
)


class AcademicSessionForm(ModelForm):
    prefix = "Academic Session"

    class Meta:
        model = AcademicSession
        fields = ["name", "current"]


class AcademicTermForm(ModelForm):
    prefix = "Academic Term"

    class Meta:
        model = AcademicTerm
        fields = ["name", "current"]


class CourseForm(ModelForm):
    prefix = "Course"

    class Meta:
        model = Course
        fields = ["name"]


class TagForm(ModelForm):
    prefix = "Class"

    class Meta:
        model = Tag
        fields = ["name"]


class CurrentSessionForm(forms.Form):
    current_session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all(),
        help_text='Click <a href="/session/create/?next=current-session/">here</a> to add new session',
    )
    current_term = forms.ModelChoiceField(
        queryset=AcademicTerm.objects.all(),
        help_text='Click <a href="/term/create/?next=current-session/">here</a> to add new term',
    )
