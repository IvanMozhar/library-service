import stripe
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from library_service import settings
from .models import Payment
from rest_framework.decorators import api_view

from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("borrowing__book_id", "user", "borrowing__user_id")
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, borrowing):
    price = borrowing.calculate_amount
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": borrowing.book_id.title,
                    },
                    "unit_amount": int(price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/api/payments/success/?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/api/payments/cancel/?session_id={CHECKOUT_SESSION_ID}",
    )

    return session


@api_view(["GET"])
def success(request):
    """Endpoint for successful payment"""
    session = stripe.checkout.Session.retrieve(request.GET.get("session_id"))
    response_data = {
        "payment_status": session.payment_status,
    }
    payment = Payment.objects.get(session_id=session.id)
    payment.status = "PAID"
    payment.save()
    return Response(response_data)


@api_view(["GET"])
def cancel(request):
    """Endpoint for canceled payment"""
    session = stripe.checkout.Session.retrieve(request.GET.get("session_id"))
    response_data = {
        "payment_status": session.payment_status,
    }
    return Response(response_data)
