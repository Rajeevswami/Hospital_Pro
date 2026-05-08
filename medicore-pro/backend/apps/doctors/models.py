"""Doctor profiles and specializations."""
import uuid
from django.db import models
from django.conf import settings


class Doctor(models.Model):
    """Doctor profile linked to a user account."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    specialization = models.CharField(max_length=200)
    qualification = models.CharField(max_length=300)
    license_number = models.CharField(max_length=100)
    department = models.ForeignKey(
        'hospitals.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors'
    )
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bio = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    max_patients_per_day = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__first_name']

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} — {self.specialization}"


class DoctorSchedule(models.Model):
    """Weekly availability schedule for a doctor."""

    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'
        SATURDAY = 5, 'Saturday'
        SUNDAY = 6, 'Sunday'

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration_minutes = models.PositiveIntegerField(default=15)
    max_appointments = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'day_of_week', 'start_time')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.doctor} — {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class DoctorLeave(models.Model):
    """Leave/unavailability records for doctors."""
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=300, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
