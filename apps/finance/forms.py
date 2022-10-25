from django.forms import inlineformset_factory, modelformset_factory

from .models import Invoice, InvoiceItem

InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=["description", "amount"], extra=1, can_delete=True
)


Invoices = modelformset_factory(Invoice, exclude=(), extra=4)
