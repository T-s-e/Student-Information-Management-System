import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.finance.models import Invoice

from .models import Other, OtherBulkUpload


class OtherListView(LoginRequiredMixin, ListView):
    model = Other
    template_name = "others/other_list.html"


class OtherDetailView(LoginRequiredMixin, DetailView):
    model = Other
    template_name = "others/other_detail.html"

    def get_context_data(self, **kwargs):
        context = super(OtherDetailView, self).get_context_data(**kwargs)
        context["payments"] = Invoice.objects.filter(other=self.object)
        return context


class OtherCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Other
    fields = "__all__"
    success_message = "New item successfully added."

    def get_form(self):
        """add date picker in forms"""
        form = super(OtherCreateView, self).get_form()
        form.fields["date_of_test"].widget = widgets.DateInput(attrs={"type": "date"})
        # form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        return form


class OtherUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Other
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(OtherUpdateView, self).get_form()
        form.fields["date_of_test"].widget = widgets.DateInput(attrs={"type": "date"})
        # form.fields["date_of_admission"].widget = widgets.DateInput(
        #     attrs={"type": "date"}
        # )
        # form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['picture'].widget = widgets.FileInput()
        return form


class OtherDeleteView(LoginRequiredMixin, DeleteView):
    model = Other
    success_url = reverse_lazy("other-list")


class OtherBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = OtherBulkUpload
    template_name = "others/others_upload.html"
    fields = ["csv_file"]
    success_url = "/other/list"
    success_message = "Successfully uploaded items"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="other_template.csv"'

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
