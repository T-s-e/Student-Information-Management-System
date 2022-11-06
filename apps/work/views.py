from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.finance.models import Invoice

from .models import Work


class WorkListView(ListView):
    model = Work


class WorkDetailView(DetailView):
    model = Work
    template_name = "work/work_detail.html"

    def get_context_data(self, **kwargs):
        context = super(WorkDetailView, self).get_context_data(**kwargs)
        context["invoices"] = Invoice.objects.filter(work=self.object)
        return context

class WorkCreateView(SuccessMessageMixin, CreateView):
    model = Work
    fields = "__all__"
    success_message = "New work successfully added"

    def get_form(self):
        """add date picker in forms"""
        form = super(WorkCreateView, self).get_form()
        # form.fields["date"].widget = widgets.DateInput(
        #     attrs={"type": "date"}
        # )
        return form


class WorkUpdateView(SuccessMessageMixin, UpdateView):
    model = Work
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(WorkUpdateView, self).get_form()
        # form.fields["date"].widget = widgets.DateInput(
        #     attrs={"type": "date"}
        # )
        return form


class WorkDeleteView(DeleteView):
    model = Work
    success_url = reverse_lazy("work-list")
