"""Subscription plans, trials, upgrades, downgrades, renewals."""
import uuid
from django.db import models


class Plan(models.Model):
    """Subscription plan definitions: Basic / Pro / Enterprise."""

    class Tier(models.TextChoices):
        BASIC = 'basic', 'Basic'
        PRO = 'pro', 'Pro'
        ENTERPRISE = 'enterprise', 'Enterprise'

    class BillingCycle(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        ANNUAL = 'annual', 'Annual'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=15, choices=Tier.choices)
    billing_cycle = models.CharField(max_length=10, choices=BillingCycle.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    max_patients = models.IntegerField(default=-1)  # -1 = unlimited
    max_staff = models.IntegerField(default=5)
    max_departments = models.IntegerField(default=3)
    features = models.JSONField(default=list)  # Feature flags
    stripe_price_id = models.CharField(max_length=100, blank=True)
    razorpay_plan_id = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.name} ({self.get_billing_cycle_display()}) — ${self.price}"


class Subscription(models.Model):
    """Hospital subscription — tracks plan, trial, billing state."""

    class Status(models.TextChoices):
        TRIALING = 'trialing', 'Trialing'
        ACTIVE = 'active', 'Active'
        PAST_DUE = 'past_due', 'Past Due'
        CANCELLED = 'cancelled', 'Cancelled'
        EXPIRED = 'expired', 'Expired'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospital = models.OneToOneField('hospitals.Hospital', on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.TRIALING)
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    # Payment gateway references
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    razorpay_subscription_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.hospital.name} — {self.plan.name} ({self.status})"


class SubscriptionEvent(models.Model):
    """Audit log for subscription lifecycle events."""

    class EventType(models.TextChoices):
        CREATED = 'created', 'Created'
        UPGRADED = 'upgraded', 'Upgraded'
        DOWNGRADED = 'downgraded', 'Downgraded'
        RENEWED = 'renewed', 'Renewed'
        CANCELLED = 'cancelled', 'Cancelled'
        PAYMENT_FAILED = 'payment_failed', 'Payment Failed'
        TRIAL_ENDED = 'trial_ended', 'Trial Ended'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    from_plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    to_plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
