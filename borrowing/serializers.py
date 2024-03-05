from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from borrowing.models import Borrow


class BorrowBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False, source="book_id")
    user = serializers.StringRelatedField(many=False, source="user_id")

    class Meta:
        model = Borrow
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ["user", "actual_return_date"]


class BorrowCreateSerializer(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrow
        fields = [
            "borrow_date",
            "expected_return_date",
            "book_id",
            "user_id"
        ]
        read_only_fields = ["user_id"]


class ReturnBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrow
        fields = (
            "actual_return_date",
        )
