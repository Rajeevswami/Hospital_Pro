"""Audit logging for compliance and security tracking."""
import uuid
from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """Immutable audit trail for all sensitive operations."""

    class Action(models.TextChoices):
        CREATE = 'create', 'Create'
        READ = 'read', 'Read'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'
        LOGIN = 'login', 'Login'
        LOGOUT = 'logout', 'Logout'
        EXPORT = 'export', 'Export'
        PERMISSION_CHANGE = 'perm_change', 'Permission Change'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=15, choices=Action.choices)
    resource_type = models.CharField(max_length=100)  # e.g., 'Patient', 'MedicalRecord'
    resource_id = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    changes = models.JSONField(default=dict, blank=True)  # {field: {old, new}}
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['resource_type', 'resource_id']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"[{self.action}] {self.resource_type} by {self.user} at {self.created_at}"
