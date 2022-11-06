from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.finance.models import Invoice

from .models import Item


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "items/item_list.html"


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "items/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context["invoices"] = Invoice.objects.filter(item=self.object)
        return context


class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    fields = "__all__"
    success_message = "New item successfully added."
    template_name = "items/item_form.html"


    def get_form(self):
        """add date picker in forms"""
        form = super(ItemCreateView, self).get_form()
        form.fields["date"].widget = widgets.DateInput(attrs={"type": "date"})
        # form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["note"].widget = widgets.Textarea(attrs={"rows": 2})
        return form


class ItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(ItemUpdateView, self).get_form()
        form.fields["date"].widget = widgets.DateInput(attrs={"type": "date"})
        # form.fields["date_of_admission"].widget = widgets.DateInput(
        #     attrs={"type": "date"}
        # )
        # form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["note"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['picture'].widget = widgets.FileInput()
        return form


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy("item-list")

