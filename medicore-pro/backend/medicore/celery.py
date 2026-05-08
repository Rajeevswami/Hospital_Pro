"""Celery configuration for MediCore Pro."""
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicore.settings.development')

app = Celery('medicore')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'check-subscription-renewals': {
        'task': 'apps.subscriptions.tasks.check_renewals',
        'schedule': 3600.0,  # Every hour
    },
    'send-appointment-reminders': {
        'task': 'apps.appointments.tasks.send_reminders',
        'schedule': 900.0,  # Every 15 minutes
    },
    'generate-daily-analytics': {
        'task': 'apps.analytics.tasks.generate_daily_report',
        'schedule': 86400.0,  # Daily
    },
    'cleanup-expired-tokens': {
        'task': 'apps.users.tasks.cleanup_expired_tokens',
        'schedule': 3600.0,
    },
}
