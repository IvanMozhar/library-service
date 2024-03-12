from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from payment_session.views import PaymentViewSet, create_checkout_session

# from payment_session.views import create_payment, success, cancel

# urlpatterns = [
#     path("create-payment/", create_payment, name="create_payment"),
#     path("success/", success, name="payment_success"),
#     path("cancel/", cancel, name="payment_cancel"),
# ]
router = routers.DefaultRouter()
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("create-checkout-session/", create_checkout_session, name="create-checkout-session")
]

app_name = "payment_session"
