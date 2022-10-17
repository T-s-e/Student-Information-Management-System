import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.finance.models import Invoice

from .models import Subject, SubjectBulkUpload


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = "subjects/subject_list.html"


class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = "subjects/subject_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SubjectDetailView, self).get_context_data(**kwargs)
        context["payments"] = Invoice.objects.filter(subject=self.object)
        return context


class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subject
    fields = "__all__"
    success_message = "New subject successfully added."

    def get_form(self):
        """add date picker in forms"""
        form = super(SubjectCreateView, self).get_form()
        form.fields["date_of_test"].widget = widgets.DateInput(attrs={"type": "date"})
        # form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        return form


class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(SubjectUpdateView, self).get_form()
        form.fields["date_of_test"].widget = widgets.DateInput(attrs={"type": "date"})
        # form.fields["date_of_admission"].widget = widgets.DateInput(
        #     attrs={"type": "date"}
        # )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['picture'].widget = widgets.FileInput()
        return form


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("subject-list")


class SubjectBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SubjectBulkUpload
    template_name = "subjects/subjects_upload.html"
    fields = ["csv_file"]
    success_url = "/subject/list"
    success_message = "Successfully uploaded subjects"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="subject_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "credit",
                "surname",
                "professor",
                "online_sources",
                "property",
                # "parent_number",
                # "address",
                # "current_class",
            ]
        )

        return response
