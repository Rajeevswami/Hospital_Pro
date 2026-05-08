"""Billing views and Stripe/Razorpay webhook handlers."""
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, permissions
from django.conf import settings
from apps.core.exceptions import IsStaff
from .models import Invoice, InvoiceItem, Payment
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY


# ── Serializers ────────────────────────────────────────────────
class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    balance_due = serializers.ReadOnlyField()
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['id', 'invoice_number', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


# ── ViewSets ───────────────────────────────────────────────────
class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        return Invoice.objects.select_related('patient').prefetch_related('items', 'payments')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsStaff]
    http_method_names = ['get', 'post', 'head']

    def get_queryset(self):
        return Payment.objects.select_related('invoice')


class CreateCheckoutSessionView(APIView):
    """Create a Stripe hosted checkout session — PCI-safe."""
    def post(self, request):
        invoice_id = request.data.get('invoice_id')
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': invoice.currency.lower(),
                    'product_data': {'name': f'Invoice {invoice.invoice_number}'},
                    'unit_amount': int(invoice.balance_due * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.data.get('success_url', 'https://medicorepro.com/payment/success'),
            cancel_url=request.data.get('cancel_url', 'https://medicorepro.com/payment/cancel'),
            metadata={'invoice_id': str(invoice.id)},
        )
        return Response({'checkout_url': session.url, 'session_id': session.id})


class StripeWebhookView(APIView):
    """Secure Stripe webhook handler — verifies signature."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            invoice_id = session['metadata'].get('invoice_id')
            if invoice_id:
                try:
                    invoice = Invoice.objects.get(id=invoice_id)
                    Payment.objects.create(
                        invoice=invoice,
                        amount=session['amount_total'] / 100,
                        currency=session['currency'].upper(),
                        gateway='stripe',
                        status='completed',
                        gateway_payment_id=session['payment_intent'],
                        gateway_response=session,
                    )
                    invoice.paid_amount += session['amount_total'] / 100
                    if invoice.paid_amount >= invoice.total:
                        invoice.status = 'paid'
                    else:
                        invoice.status = 'partial'
                    invoice.save()
                except Invoice.DoesNotExist:
                    pass

        return Response({'received': True})
