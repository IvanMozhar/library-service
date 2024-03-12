import stripe
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from library_service import settings
from .models import Payment
from rest_framework.decorators import api_view

from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, borrowing):
    price = borrowing.calculate_amount
    session = stripe.checkout.Session.create(
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": borrowing.book_id.title,
                },
                "unit_amount": int(price * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://127.0.0.1:8000/api/payments/success/",
        cancel_url="http://127.0.0.1:8000/api/payments/cancel/",
    )

    return session


@api_view(["GET"])
def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return JsonResponse({"message": "Payment succeded"})


@api_view(["GET"])
def cancel(request):
    return JsonResponse({"message": "Payment cancelled or failed"})
