from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowing.models import Borrow
from borrowing.serializers import BorrowBookSerializer

User = get_user_model()
BORROW_URL = reverse("borrowing:borrow-list")


def sample_borrow(**params):
    book = Book.objects.create(
        title="Test",
        author="Test Author",
        cover="Softcover",
        inventory=1,
        daily_fee=20,
    )
    user = User.objects.create_user(email="test@example.com", password="testpass123")
    defaults = {
        "borrow_date": "2024-03-20",
        "expected_return_date": "2024-03-25",
        "book_id": book,
        "user_id": user,
    }
    defaults.update(params)
    return Borrow.objects.create(**defaults)


class UnauthenticatedBorrowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_borrows(self):
        sample_borrow(user_id=self.user)
        res = self.client.get(BORROW_URL)

        borrows = Borrow.objects.order_by("id")
        serializer = BorrowBookSerializer(borrows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_borrow_by_is_active(self):
        url = BORROW_URL + "?is_active=True"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_borrow_by_user(self):
        self.client.force_authenticate(user=self.user)
        url = BORROW_URL + f"?user_id={self.user.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
