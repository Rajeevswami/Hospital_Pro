"""Razorpay webhook handler placeholder."""
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

class RazorpayWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # TODO: Verify Razorpay webhook signature and process payment events
        return Response({'received': True})

urlpatterns = [path('', RazorpayWebhookView.as_view(), name='razorpay-webhook')]
