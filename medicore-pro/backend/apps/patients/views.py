"""Patient serializers, views, and URL config."""
from rest_framework import serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.exceptions import IsStaff, IsPatientOwner
from .models import Patient, MedicalRecord, Prescription


# ── Serializers ────────────────────────────────────────────────
class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id', 'patient_id', 'created_at', 'updated_at']

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


# ── ViewSets ───────────────────────────────────────────────────
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'blood_group', 'is_active']
    search_fields = ['first_name', 'last_name', 'patient_id', 'phone', 'email']
    ordering_fields = ['created_at', 'last_name']

    def get_queryset(self):
        return Patient.objects.all()

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsStaff | IsPatientOwner]

    def get_queryset(self):
        qs = MedicalRecord.objects.select_related('patient', 'doctor')
        patient_id = self.request.query_params.get('patient')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        if self.request.user.role == 'patient':
            qs = qs.filter(patient__user=self.request.user)
        return qs

class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsStaff | IsPatientOwner]

    def get_queryset(self):
        qs = Prescription.objects.select_related('patient', 'doctor')
        if self.request.user.role == 'patient':
            qs = qs.filter(patient__user=self.request.user)
        return qs
