"""Custom User model with role-based access control and MFA support."""
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user with RBAC roles and MFA."""

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrator'
        DOCTOR = 'doctor', 'Doctor'
        STAFF = 'staff', 'Staff'
        PATIENT = 'patient', 'Patient'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Use email instead
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STAFF)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    hospital = models.ForeignKey(
        'hospitals.Hospital', on_delete=models.CASCADE, null=True, blank=True, related_name='users'
    )

    # MFA
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=32, blank=True)  # TOTP secret
    mfa_backup_codes = models.JSONField(default=list, blank=True)

    # Security
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    password_changed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_doctor(self):
        return self.role == self.Role.DOCTOR
