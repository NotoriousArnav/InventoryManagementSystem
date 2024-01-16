from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from inventory.models import Product
import uuid

# Create your models here.
class Customer(models.Model):
    id = models.UUIDField(
                default=uuid.uuid4,
                primary_key=True,
                editable=False
            )
    user = models.ForeignKey(
                User,
                on_delete=models.CASCADE,
                null=True
            )
    phone_number_cc = models.IntegerField(
                default=91,
            )
    phone_number = models.IntegerField(
                default = 0
            )
    email = models.CharField(
                max_length=201,
                null=True
            )

    def __str__(self):
        return f"{self.user.first_name+' '+self.user.last_name} - {str(self.phone_number)[:4]}"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.FloatField(default=0.0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"

class Invoice(models.Model):
    id = models.UUIDField(
                default = uuid.uuid4,
                editable = False,
                primary_key = True
            )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    invoice_date = models.DateTimeField(default=timezone.now)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_status = models.BooleanField(
                default=False
            )

    def final_amount(self):
        total = sum(item.subtotal() for item in self.invoiceitem_set.all())
        discount_amount = self.calculated_discount()
        return total - discount_amount

    def total_amount(self):
        return sum(item.subtotal() for item in self.invoiceitem_set.all())

    def calculated_discount(self):
        total_amount = self.total_amount()
        if self.coupon and self.coupon.is_valid():
            return total_amount * (self.coupon.discount_percentage / 100)
        return 0.0

    def save(self, *args, **kwargs):
        # Check if transaction_status has changed to True
        if self.transaction_status and not self._state.adding:
            # Iterate over invoice items and update product quantities
            for item in self.invoiceitem_set.all():
                product = item.product
                new_qty = product.qty - item.quantity
                if new_qty < 0:
                    raise ValueError(f"Not enough stock for product: {product.name}")
                product.qty = new_qty
                product.save()

        # Save the invoice
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice-{str(self.id)[:5]} ({self.customer.user.first_name if self.customer else 'No Customer'})"


class InvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.invoice}-{self.product}"

    def subtotal(self):
        return self.product.price * self.quantity

