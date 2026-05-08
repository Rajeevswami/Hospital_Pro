from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, PaymentViewSet, CreateCheckoutSessionView

app_name = 'billing'
router = DefaultRouter()
router.register('invoices', InvoiceViewSet, basename='invoice')
router.register('payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', CreateCheckoutSessionView.as_view(), name='checkout'),
]
