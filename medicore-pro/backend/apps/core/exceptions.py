"""Core utilities — encryption, permissions, exception handling."""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import permissions, status
from cryptography.fernet import Fernet
from django.conf import settings


# ── AES Encryption Helper ──────────────────────────────────────
class FieldEncryptor:
    """Encrypt/decrypt sensitive fields using Fernet (AES-128-CBC)."""
    def __init__(self):
        key = settings.ENCRYPTION_KEY
        if key:
            self.fernet = Fernet(key.encode() if isinstance(key, str) else key)
        else:
            self.fernet = None

    def encrypt(self, value: str) -> str:
        if not self.fernet or not value:
            return value
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        if not self.fernet or not value:
            return value
        try:
            return self.fernet.decrypt(value.encode()).decode()
        except Exception:
            return value

encryptor = FieldEncryptor()


# ── Custom Permissions ─────────────────────────────────────────
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('admin', 'doctor')

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('admin', 'doctor', 'staff')

class IsPatientOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ('admin', 'doctor', 'staff'):
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'patient') and hasattr(obj.patient, 'user'):
            return obj.patient.user == request.user
        return False


# ── Custom Exception Handler ──────────────────────────────────
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'detail': response.data,
            }
        }
    return response
