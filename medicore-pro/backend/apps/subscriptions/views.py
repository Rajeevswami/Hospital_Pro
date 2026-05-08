"""Subscription management — upgrade, downgrade, cancel, renew."""
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from apps.core.exceptions import IsAdmin
from .models import Plan, Subscription, SubscriptionEvent


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['id', 'hospital', 'created_at', 'updated_at']


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)
    permission_classes = []  # Public


class SubscriptionView(APIView):
    """Retrieve current hospital subscription."""
    permission_classes = [IsAdmin]

    def get(self, request):
        try:
            sub = Subscription.objects.select_related('plan').get(hospital=request.user.hospital)
            return Response(SubscriptionSerializer(sub).data)
        except Subscription.DoesNotExist:
            return Response({'error': 'No subscription found.'}, status=status.HTTP_404_NOT_FOUND)


class UpgradeDowngradeView(APIView):
    """Change subscription plan (upgrade/downgrade)."""
    permission_classes = [IsAdmin]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        try:
            new_plan = Plan.objects.get(id=plan_id, is_active=True)
            sub = Subscription.objects.get(hospital=request.user.hospital)
        except (Plan.DoesNotExist, Subscription.DoesNotExist):
            return Response({'error': 'Invalid plan or no subscription.'}, status=status.HTTP_400_BAD_REQUEST)

        old_plan = sub.plan
        event_type = 'upgraded' if new_plan.price > old_plan.price else 'downgraded'
        sub.plan = new_plan
        sub.save(update_fields=['plan', 'updated_at'])

        SubscriptionEvent.objects.create(
            subscription=sub, event_type=event_type,
            from_plan=old_plan, to_plan=new_plan,
        )
        return Response({'success': True, 'message': f'Plan {event_type} to {new_plan.name}.'})


class CancelSubscriptionView(APIView):
    """Cancel subscription at end of billing period."""
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            sub = Subscription.objects.get(hospital=request.user.hospital)
        except Subscription.DoesNotExist:
            return Response({'error': 'No subscription.'}, status=status.HTTP_404_NOT_FOUND)

        sub.cancel_at_period_end = True
        sub.save(update_fields=['cancel_at_period_end', 'updated_at'])
        SubscriptionEvent.objects.create(subscription=sub, event_type='cancelled')
        return Response({'success': True, 'message': 'Subscription will cancel at period end.'})
