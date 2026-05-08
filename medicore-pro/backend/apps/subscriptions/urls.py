from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SubscriptionView, UpgradeDowngradeView, CancelSubscriptionView

app_name = 'subscriptions'
router = DefaultRouter()
router.register('plans', PlanViewSet, basename='plan')

urlpatterns = [
    path('', include(router.urls)),
    path('current/', SubscriptionView.as_view(), name='current'),
    path('change-plan/', UpgradeDowngradeView.as_view(), name='change-plan'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel'),
]
