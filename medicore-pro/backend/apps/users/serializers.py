"""User serializers — registration, login, profile, MFA."""
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=10)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name', 'role', 'phone']

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone', 'avatar',
                  'mfa_enabled', 'hospital', 'created_at']
        read_only_fields = ['id', 'email', 'role', 'created_at']


class MFASetupSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6, min_length=6)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=10)
