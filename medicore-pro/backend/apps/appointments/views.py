"""Appointment serializers, views, URL config."""
from rest_framework import serializers, viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.exceptions import IsStaff
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def validate(self, data):
        if data.get('start_time') and data.get('end_time'):
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError('End time must be after start time.')
        # Check for conflicts
        conflicts = Appointment.objects.filter(
            doctor=data.get('doctor'),
            appointment_date=data.get('appointment_date'),
            start_time__lt=data.get('end_time'),
            end_time__gt=data.get('start_time'),
            status__in=['scheduled', 'confirmed'],
        )
        if self.instance:
            conflicts = conflicts.exclude(pk=self.instance.pk)
        if conflicts.exists():
            raise serializers.ValidationError('This time slot conflicts with another appointment.')
        return data


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'doctor', 'patient', 'appointment_date']
    ordering_fields = ['appointment_date', 'start_time', 'created_at']

    def get_queryset(self):
        qs = Appointment.objects.select_related('patient', 'doctor', 'department')
        user = self.request.user
        if user.role == 'doctor':
            qs = qs.filter(doctor__user=user)
        elif user.role == 'patient':
            qs = qs.filter(patient__user=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appt = self.get_object()
        if appt.status in ('completed', 'cancelled'):
            return Response({'error': 'Cannot cancel this appointment.'}, status=status.HTTP_400_BAD_REQUEST)
        appt.status = Appointment.Status.CANCELLED
        appt.save(update_fields=['status', 'updated_at'])
        return Response({'success': True, 'message': 'Appointment cancelled.'})

    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        appt = self.get_object()
        appt.status = Appointment.Status.CHECKED_IN
        appt.save(update_fields=['status', 'updated_at'])
        return Response({'success': True})
