from rest_framework import serializers
from payment_session.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    borrowing = serializers.StringRelatedField(many=False)
    user = serializers.CharField(source="user.email")

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "session_url",
            "session_id",
            "borrowing",
            "user",
        ]


class PaymentBorrowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "session_url",
            "session_id",
        ]
