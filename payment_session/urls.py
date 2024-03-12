from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from payment_session.views import PaymentViewSet, create_checkout_session

from payment_session.views import success, cancel

router = routers.DefaultRouter()
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
]

app_name = "payment_session"
