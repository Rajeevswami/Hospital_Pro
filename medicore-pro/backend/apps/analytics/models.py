"""Analytics snapshot models for dashboard metrics."""
import uuid
from django.db import models


class DailyAnalytics(models.Model):
    """Pre-computed daily metrics for the analytics dashboard."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(unique=True)
    total_appointments = models.IntegerField(default=0)
    completed_appointments = models.IntegerField(default=0)
    cancelled_appointments = models.IntegerField(default=0)
    no_show_count = models.IntegerField(default=0)
    new_patients = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    outstanding_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    bed_occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    avg_wait_time_minutes = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    department_breakdown = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Daily analytics'

    def __str__(self):
        return f"Analytics {self.date}"
