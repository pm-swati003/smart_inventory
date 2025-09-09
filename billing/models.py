from django.db import models
from products.models import Product
from customers.models import Customer
from decimal import Decimal

PAYMENT_CHOICES = [
    ("CASH", "Cash"),
    ("CARD", "Card"),
    ("UPI", "UPI"),
]

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="CASH")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_no

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = (self.price or self.product.price) * self.quantity
        super().save(*args, **kwargs)
