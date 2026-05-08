"""Patient management models with encrypted sensitive data."""
import uuid
from django.db import models
from django.conf import settings


class Patient(models.Model):
    """Patient record — linked to a user account optionally."""

    class BloodGroup(models.TextChoices):
        A_POS = 'A+', 'A+'
        A_NEG = 'A-', 'A-'
        B_POS = 'B+', 'B+'
        B_NEG = 'B-', 'B-'
        AB_POS = 'AB+', 'AB+'
        AB_NEG = 'AB-', 'AB-'
        O_POS = 'O+', 'O+'
        O_NEG = 'O-', 'O-'

    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    patient_id = models.CharField(max_length=20, unique=True)  # Hospital-generated ID
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    insurance_provider = models.CharField(max_length=200, blank=True)
    insurance_policy_number = models.CharField(max_length=100, blank=True)  # Encrypted at app layer
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class MedicalRecord(models.Model):
    """Electronic Health Record — encrypted sensitive fields."""

    class RecordType(models.TextChoices):
        CONSULTATION = 'consultation', 'Consultation'
        LAB_RESULT = 'lab_result', 'Lab Result'
        IMAGING = 'imaging', 'Imaging'
        SURGERY = 'surgery', 'Surgery'
        DISCHARGE = 'discharge', 'Discharge Summary'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True)
    record_type = models.CharField(max_length=20, choices=RecordType.choices)
    title = models.CharField(max_length=300)
    diagnosis = models.TextField(blank=True)  # Encrypted
    notes = models.TextField(blank=True)  # Encrypted
    attachments = models.JSONField(default=list, blank=True)  # S3 file keys
    vitals = models.JSONField(default=dict, blank=True)
    is_confidential = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.patient}"


class Prescription(models.Model):
    """Prescription linked to a medical record."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True)
    medications = models.JSONField(default=list)  # [{name, dosage, frequency, duration}]
    instructions = models.TextField(blank=True)
    is_dispensed = models.BooleanField(default=False)
    dispensed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Rx for {self.patient} by Dr. {self.doctor}"
