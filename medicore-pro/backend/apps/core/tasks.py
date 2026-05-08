"""Celery tasks for background job processing."""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_appointment_reminders():
    """Send reminders for appointments within the next 2 hours."""
    from apps.appointments.models import Appointment
    from apps.notifications.models import Notification
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    upcoming = Appointment.objects.filter(
        appointment_date=timezone.now().date(),
        start_time__lte=(timezone.now() + timedelta(hours=2)).time(),
        start_time__gte=timezone.now().time(),
        status='scheduled',
        reminder_sent=False,
    ).select_related('patient', 'doctor')

    channel_layer = get_channel_layer()
    for appt in upcoming:
        # Notify patient
        if appt.patient.user:
            notif = Notification.objects.create(
                user=appt.patient.user,
                category='appointment',
                title='Upcoming Appointment',
                message=f'Your appointment with Dr. {appt.doctor} is at {appt.start_time}.',
                data={'appointment_id': str(appt.id)},
            )
            async_to_sync(channel_layer.group_send)(
                f'notifications_{appt.patient.user.id}',
                {'type': 'send_notification', 'data': {'title': notif.title, 'message': notif.message}}
            )
        appt.reminder_sent = True
        appt.save(update_fields=['reminder_sent'])


@shared_task
def check_subscription_renewals():
    """Check and process subscription renewals / expirations."""
    from apps.subscriptions.models import Subscription, SubscriptionEvent

    now = timezone.now()
    expired = Subscription.objects.filter(
        current_period_end__lte=now,
        status='active',
        cancel_at_period_end=True,
    )
    for sub in expired:
        sub.status = 'cancelled'
        sub.cancelled_at = now
        sub.save(update_fields=['status', 'cancelled_at', 'updated_at'])
        SubscriptionEvent.objects.create(subscription=sub, event_type='cancelled')


@shared_task
def generate_daily_analytics():
    """Generate daily analytics snapshot."""
    from apps.analytics.models import DailyAnalytics
    from apps.appointments.models import Appointment
    from apps.patients.models import Patient
    from apps.billing.models import Invoice

    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    appts = Appointment.objects.filter(appointment_date=yesterday)
    DailyAnalytics.objects.update_or_create(
        date=yesterday,
        defaults={
            'total_appointments': appts.count(),
            'completed_appointments': appts.filter(status='completed').count(),
            'cancelled_appointments': appts.filter(status='cancelled').count(),
            'no_show_count': appts.filter(status='no_show').count(),
            'new_patients': Patient.objects.filter(created_at__date=yesterday).count(),
            'total_revenue': Invoice.objects.filter(
                created_at__date=yesterday, status='paid'
            ).aggregate(total=models.Sum('total'))['total'] or 0,
        }
    )
