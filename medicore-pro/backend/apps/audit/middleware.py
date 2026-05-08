"""Audit log middleware — automatically tracks API operations."""
from django.utils.deprecation import MiddlewareMixin
from .models import AuditLog


class AuditLogMiddleware(MiddlewareMixin):
    """Logs write operations on sensitive API endpoints."""

    AUDITED_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')
    AUDITED_PATHS = ('/api/v1/patients/', '/api/v1/appointments/', '/api/v1/billing/')

    def process_response(self, request, response):
        if (request.method in self.AUDITED_METHODS
                and any(request.path.startswith(p) for p in self.AUDITED_PATHS)
                and hasattr(request, 'user') and request.user.is_authenticated
                and response.status_code < 400):

            action_map = {'POST': 'create', 'PUT': 'update', 'PATCH': 'update', 'DELETE': 'delete'}

            AuditLog.objects.create(
                user=request.user,
                action=action_map.get(request.method, 'update'),
                resource_type=request.path.split('/')[3] if len(request.path.split('/')) > 3 else '',
                description=f"{request.method} {request.path}",
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            )
        return response

    @staticmethod
    def _get_client_ip(request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')
