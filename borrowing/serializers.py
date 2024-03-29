from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from borrowing.models import Borrow
from payment_session.models import Payment
from payment_session.serializers import PaymentBorrowSerializer


class BorrowBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False, source="book_id")
    user = serializers.StringRelatedField(many=False, source="user_id")
    payment_details = serializers.SerializerMethodField()

    class Meta:
        model = Borrow
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payment_details",
        )
        read_only_fields = ["user", "actual_return_date"]

    def get_payment_details(self, obj):
        return obj.get_payment_session()


class BorrowCreateSerializer(serializers.ModelSerializer):
    """Create borrowing"""

    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrow
        fields = ["borrow_date", "expected_return_date", "book_id", "user_id"]
        read_only_fields = ["user_id"]


class ReturnBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrow
        fields = ("actual_return_date",)
