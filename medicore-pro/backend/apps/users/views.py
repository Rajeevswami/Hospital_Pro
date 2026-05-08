"""User views — authentication, profile, MFA setup."""
import pyotp
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer,
    MFASetupSerializer, ChangePasswordSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'success': True,
            'message': 'Account created successfully.',
            'user_id': str(user.id),
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class MFASetupView(APIView):
    """Enable TOTP-based MFA."""

    def get(self, request):
        secret = pyotp.random_base32()
        request.user.mfa_secret = secret
        request.user.save(update_fields=['mfa_secret'])
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=request.user.email, issuer_name='MediCore Pro'
        )
        return Response({'secret': secret, 'qr_uri': provisioning_uri})

    def post(self, request):
        serializer = MFASetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        totp = pyotp.TOTP(request.user.mfa_secret)
        if totp.verify(serializer.validated_data['otp_code']):
            request.user.mfa_enabled = True
            request.user.save(update_fields=['mfa_enabled'])
            return Response({'success': True, 'message': 'MFA enabled.'})
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Wrong current password'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'success': True, 'message': 'Password changed.'})
