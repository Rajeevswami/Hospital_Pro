"""User app URL routes."""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('mfa/setup/', views.MFASetupView.as_view(), name='mfa-setup'),
    path('password/change/', views.ChangePasswordView.as_view(), name='change-password'),
]
