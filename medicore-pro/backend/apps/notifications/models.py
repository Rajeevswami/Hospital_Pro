"""Real-time notifications and WebSocket support."""
import uuid
from django.db import models
from django.conf import settings


class Notification(models.Model):
    class Category(models.TextChoices):
        APPOINTMENT = 'appointment', 'Appointment'
        BILLING = 'billing', 'Billing'
        SYSTEM = 'system', 'System'
        ALERT = 'alert', 'Alert'
        SCHEDULE = 'schedule', 'Schedule Change'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    category = models.CharField(max_length=15, choices=Category.choices)
    title = models.CharField(max_length=300)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)  # Action URL, entity ID, etc.
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'is_read'])]

    def __str__(self):
        return f"[{self.category}] {self.title} → {self.user}"
