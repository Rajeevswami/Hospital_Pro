"""MediCore Pro — Root URL Configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/hospitals/', include('apps.hospitals.urls')),
    path('api/v1/patients/', include('apps.patients.urls')),
    path('api/v1/doctors/', include('apps.doctors.urls')),
    path('api/v1/appointments/', include('apps.appointments.urls')),
    path('api/v1/billing/', include('apps.billing.urls')),
    path('api/v1/subscriptions/', include('apps.subscriptions.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/audit/', include('apps.audit.urls')),

    # Webhooks (outside versioned API)
    path('webhooks/stripe/', include('apps.billing.webhook_urls')),
    path('webhooks/razorpay/', include('apps.billing.webhook_urls_razorpay')),

    # API Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Health Check
    path('health/', include('health_check.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
