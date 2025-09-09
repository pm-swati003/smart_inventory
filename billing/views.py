from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvoiceForm, InvoiceItemFormSet
from .models import Invoice, InvoiceItem
from products.models import Product
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

@login_required
def invoice_list(request):
    qs = Invoice.objects.all().order_by("-created_at")
    return render(request, "billing/invoice_list.html", {"invoices": qs})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, "billing/invoice_detail.html", {"invoice": invoice})

@login_required
def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    invoice = form.save(commit=False)
                    invoice.total = Decimal("0.00")
                    invoice.save()
                    formset.instance = invoice
                    items = formset.save(commit=False)

                    # validate stock
                    for item in items:
                        product = Product.objects.select_for_update().get(pk=item.product.pk)
                        if product.stock < item.quantity:
                            raise ValueError(f"Not enough stock for {product.name}")

                    # now save items and update stock
                    for item in items:
                        if not item.price:
                            item.price = item.product.price
                        item.invoice = invoice
                        item.save()
                        # decrement stock
                        product = Product.objects.get(pk=item.product.pk)
                        product.stock = product.stock - item.quantity
                        product.save()
                        invoice.total += item.subtotal

                    invoice.tax = (invoice.total * Decimal("0.18")).quantize(Decimal("0.01"))  # example 18% GST
                    invoice.total = (invoice.total + invoice.tax - invoice.discount).quantize(Decimal("0.01"))
                    invoice.save()
                    messages.success(request, "Invoice created successfully.")
                    return redirect("billing:invoice_detail", pk=invoice.pk)
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Please fix the form errors.")
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
    return render(request, "billing/invoice_create.html", {"form": form, "formset": formset})
