"""Billing, invoices, and payment records."""
import uuid
from django.db import models
from django.conf import settings


class Invoice(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SENT = 'sent', 'Sent'
        PAID = 'paid', 'Paid'
        PARTIAL = 'partial', 'Partially Paid'
        OVERDUE = 'overdue', 'Overdue'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=30, unique=True)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='invoices')
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.DRAFT)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    due_date = models.DateField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    insurance_claim_id = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"INV-{self.invoice_number} — {self.patient}"

    @property
    def balance_due(self):
        return self.total - self.paid_amount


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=300)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Payment records — no raw card data stored (PCI-safe)."""

    class Gateway(models.TextChoices):
        STRIPE = 'stripe', 'Stripe'
        RAZORPAY = 'razorpay', 'Razorpay'
        CASH = 'cash', 'Cash'
        INSURANCE = 'insurance', 'Insurance'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    gateway = models.CharField(max_length=15, choices=Gateway.choices)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    gateway_payment_id = models.CharField(max_length=200, blank=True)  # Stripe/Razorpay ID
    gateway_response = models.JSONField(default=dict, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} — {self.amount} {self.currency} via {self.gateway}"
