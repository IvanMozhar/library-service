from rest_framework import serializers
from payment_session.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "status", "type", "stripe_url", "borrowing", "user"]
