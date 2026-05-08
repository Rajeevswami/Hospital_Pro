"""Appointment booking and management."""
import uuid
from django.db import models
from django.conf import settings


class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        CONFIRMED = 'confirmed', 'Confirmed'
        CHECKED_IN = 'checked_in', 'Checked In'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        NO_SHOW = 'no_show', 'No Show'

    class Priority(models.TextChoices):
        NORMAL = 'normal', 'Normal'
        URGENT = 'urgent', 'Urgent'
        EMERGENCY = 'emergency', 'Emergency'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='appointments')
    department = models.ForeignKey('hospitals.Department', on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.SCHEDULED)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.NORMAL)
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_follow_up = models.BooleanField(default=False)
    parent_appointment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date', 'start_time']
        indexes = [
            models.Index(fields=['doctor', 'appointment_date']),
            models.Index(fields=['patient', 'appointment_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.patient} → Dr. {self.doctor} on {self.appointment_date} {self.start_time}"
