import stripe
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from library_service import settings
from .models import Payment
from payment_session.stripe import create_stripe_session
from rest_framework.decorators import api_view

from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, borrowing):
    session = stripe.checkout.Session.create(
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Coffee",
                },
                "unit_amount": 1,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://127.0.0.1:8000",
        cancel_url="http://127.0.0.1:8000",
    )
    payment = Payment.objects.create(
        status="PENDING",
        type="PAYMENT",
        session_url=session.url,
        session_id=session.id,
        borrowing=borrowing,
        money_to_pay=amount,
        user=request.user
    )

    return redirect(session.url, code=303)

# @api_view(["POST"])
# def create_payment(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=["card"],
#         line_items=[
#             {
#                 "price_data": {
#                     "currency": "usd",
#                     "unit_amount": 2000,
#                 },
#                 "quantity": 1,
#             }
#         ],
#         mode="payment",
#         success_url="http://127.0.0.1:8000/success",
#         cancel_url="http://127.0.0.1:8000/cancel",
#     )
#
#     return redirect(checkout_session.url, code=303)
#
#
# @api_view(["GET"])
# def success(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     session_id = request.GET.get("session_id")
#     session = stripe.checkout.Session.retrieve(session_id)
#     customer = stripe.Customer.retrieve(session.customer)
#     user_id = request.user.id
#     user_payment = Payment.objects.get(user_id=user_id)
#     user_payment.stripe_url = session_id
#     return JsonResponse({"message": "Payment succeded"})
#
#
# @api_view(["GET"])
# def cancel(request):
#     return JsonResponse({"message": "Payment cancelled or failed"})
