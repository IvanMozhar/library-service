from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowBookViewSet

# urlpatterns = [
#     path(
#         "borrowings/",
#         BorrowBookViewSet.as_view({"get": "list"}),
#         name="borrow-list"
#     ),
#     path(
#         "borrowings/<int:pk>/",
#         BorrowBookViewSet.as_view({"get": "retrieve", "post": "create"}),
#         name="borrow-detail"
#     ),
# ]

router = routers.DefaultRouter()
router.register("borrowings", BorrowBookViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "borrowing"
