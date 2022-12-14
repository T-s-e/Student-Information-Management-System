from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.forms import widgets

from apps.others.models import Item
from apps.subjects.models import Subject

from .forms import InvoiceItemFormset, InvoiceSubject,InvoiceItem, InvoiceWork,InvoiceDueDate, InvoiceReceiptFormSet, InvoiceDueDateFormset, InvoiceSubjectFormset, Invoices, InvoiceWorkFormset
from .models import Invoice, InvoiceItem, InvoiceSubject, Receipt, InvoiceWork, InvoiceDueDate


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = ["subject", "work", "item", "session", "term", "due_date", "status"]
    success_url = "/finance/list"

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = InvoiceItemFormset(
                self.request.POST, prefix="invoiceitem_set"
            )
            context["subjects"] = InvoiceSubjectFormset(
                self.request.POST, prefix="invoicesubject_set"
            )
            context["work"] = InvoiceWorkFormset(
                self.request.POST, prefix="invoicework_set"
            )
            context["receipts"] = InvoiceReceiptFormSet(
                self.request.POST, instance=self.object
            )
            # context["due_date"] = self.request.POST.due_date
            # context["due_date"].widget = widgets.DateInput(attrs={"type": "date"})
            # context["due_date"] = InvoiceDueDateFormset(
            #     self.request.POST, prefix="invoicedue_date_set"
            # )
        else:
            context["items"] = InvoiceItemFormset(prefix="invoiceitem_set")
            context["subjects"] = InvoiceSubjectFormset(prefix="invoicesubject_set")
            context["work"] = InvoiceWorkFormset(prefix="invoicework_set")
            context["receipts"] = InvoiceReceiptFormSet(instance=self.object)

            # context["due_date"].widget = widgets.DateInput(attrs={"type": "date"})
            # context["due_date"] = InvoiceDueDateFormset(prefix="invoicedue_date_set")
            # context["due_date"] = self.request.POST.due_date

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["items"]
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    fields = ["item", "session", "term", "subject", "work", "due_date"]

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        # context["receipts"] = Receipt.objects.filter(invoice=self.object)
        context["items"] = InvoiceItem.objects.filter(invoice=self.object)
        context["subjects"] = InvoiceSubject.objects.filter(invoice=self.object)
        context["work"] = InvoiceWork.objects.filter(invoice=self.object)

        # context["due_date"] = InvoiceDueDate.objects.filter(invoice=self.object)

        return context


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    fields = ["item", "session", "term", "subject", "work", "due_date"]

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["receipts"] = InvoiceReceiptFormSet(
                self.request.POST, instance=self.object
            )
            context["items"] = InvoiceItemFormset(
                self.request.POST, instance=self.object
            )
            context["subjects"] = InvoiceSubjectFormset(
                self.request.POST, instance=self.object
            )
            context["work"] = InvoiceWorkFormset(
                self.request.POST, instance=self.object
            )
            # context["due_date"] = InvoiceDueDateFormset(
            #     self.request.POST, instance=self.object
            # )
        else:
            context["receipts"] = InvoiceReceiptFormSet(instance=self.object)
            context["items"] = InvoiceItemFormset(instance=self.object)
            context["subjects"] = InvoiceSubjectFormset(instance=self.object)
            context["work"] = InvoiceWorkFormset(instance=self.object)
            # context["due_date"] = InvoiceDueDateFormset(instance=self.object)
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["items"]
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     formset = context["receipts"]
    #     itemsformset = context["items"]
    #     if form.is_valid() and formset.is_valid() and itemsformset.is_valid():
    #         form.save()
    #         formset.save()
    #         itemsformset.save()
    #     return super().form_valid(form)


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("invoice-list")


class ReceiptCreateView(LoginRequiredMixin, CreateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        obj.invoice = invoice
        obj.save()
        return redirect("invoice-list")

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        context["invoice"] = invoice
        return context


class ReceiptUpdateView(LoginRequiredMixin, UpdateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")


class ReceiptDeleteView(LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy("invoice-list")


@login_required
def bulk_invoice(request):
    return render(request, "finance/bulk_invoice.html")
