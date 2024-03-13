from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowBookViewSet


router = routers.DefaultRouter()
router.register("borrowings", BorrowBookViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "borrowing"
