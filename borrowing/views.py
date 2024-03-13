from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from books.models import Book
from borrowing.commands import notify
from borrowing.models import Borrow
from borrowing.permissions import IsOwnerOrReadOnly
from borrowing.serializers import (
    BorrowBookSerializer,
    BorrowCreateSerializer,
    ReturnBookSerializer,
)
from payment_session.models import Payment
from payment_session.views import create_checkout_session


class BorrowBookViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Borrow.objects.all()
    serializer_class = BorrowBookSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return BorrowBookSerializer
        if self.action == "return_book":
            return ReturnBookSerializer
        return BorrowCreateSerializer

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        queryset = self.queryset

        if is_active == "True":
            queryset = queryset.filter(actual_return_date=None)

        if user_id and self.request.user.is_staff:
            queryset = queryset.filter(user_id=user_id)

        if self.request.user.is_staff:
            return queryset
        else:
            return queryset.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data["book_id"]
        with transaction.atomic():
            book = Book.objects.select_for_update().get(pk=book_id.pk)
            if book.inventory > 0:
                serializer.validated_data["user_id"] = request.user
                borrow, created = Borrow.objects.get_or_create(
                    **serializer.validated_data
                )
                book.inventory -= 1
                book.save()
                checkout_session = create_checkout_session(request, borrow)
                if created:
                    Payment.objects.get_or_create(
                        status="PENDING",
                        type="PAYMENT",
                        session_url=checkout_session.url,
                        session_id=checkout_session.id,
                        borrowing=borrow,
                        money_to_pay=borrow.calculate_amount,
                        user=request.user,
                    )
                    message = (
                        f"A new borrow record has been created:\n"
                        f"User: {borrow.user_id.email}\n"
                        f"Book: {borrow.book_id.__str__()}\n"
                        f"Borrow Date: {borrow.borrow_date}\n"
                        f"Expected Return Date: {borrow.expected_return_date}"
                    )
                    notify(message=message)
                response_data = serializer.data
                response_data["payment_url"] = checkout_session.url
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"detail": "This book is out of stock."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(
        methods=["POST"],
        url_path="return",
        detail=True,
        serializer_class=ReturnBookSerializer,
        permission_classes=[IsOwnerOrReadOnly],
    )
    def return_book(self, request, pk=None):
        """Endpoint for returning book"""
        borrow = self.get_object()
        serializer = ReturnBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            if borrow.actual_return_date:
                return Response(
                    {"detail": "You have already returned this book."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            borrow.actual_return_date = serializer.validated_data["actual_return_date"]
            borrow.save()
            if borrow.actual_return_date > borrow.expected_return_date:
                checkout_session = create_checkout_session(request, borrow)
                payment = Payment.objects.get(borrowing=borrow)
                payment.money_to_pay = int(borrow.calculate_amount)
                payment.session_url = checkout_session.url
                payment.session_id = checkout_session.id
                payment.type = "FINE"
                payment.save()
            book = borrow.book_id
            book.inventory += 1
            book.save()
        response_data = {
            "detail": "You have returned the book late. Additional payment required.",
            "payment_url": checkout_session.url,
            "session_id": checkout_session.id,
            "new_price": payment.money_to_pay,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by active borrowings (ex. ?active=True)",
            ),
            OpenApiParameter(
                "user_id",
                type=OpenApiTypes.INT,
                description=("Filter by user_id (only for admin)" "(ex. ?user_id=2)"),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
