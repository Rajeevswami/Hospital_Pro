"""Patient URL routes."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, MedicalRecordViewSet, PrescriptionViewSet

app_name = 'patients'
router = DefaultRouter()
router.register('', PatientViewSet, basename='patient')
router.register('records', MedicalRecordViewSet, basename='medical-record')
router.register('prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [path('', include(router.urls))]
