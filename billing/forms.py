from django import forms
from .models import Invoice, InvoiceItem
from django.forms import inlineformset_factory

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["invoice_no", "customer", "discount", "payment_mode"]

InvoiceItemFormSet = inlineformset_factory(
    Invoice, InvoiceItem,
    fields=("product", "quantity", "price"),
    extra=2,
    can_delete=True
)
