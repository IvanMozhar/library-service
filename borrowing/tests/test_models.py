from django.contrib.auth import get_user_model
from django.test import TestCase

from books.models import Book
from borrowing.models import Borrow

User = get_user_model()


class BorrowTestCase(TestCase):
    def setUp(self):
        Borrow.objects.create(
            borrow_date="2024-03-20",
            expected_return_date="2024-03-25",
            book_id=Book.objects.create(
                title="Test",
                author="Test Author",
                cover="Softcover",
                inventory=1,
                daily_fee=20,
            ),
            user_id=User.objects.create_user(
                email="test@example.com", password="testpass123"
            ),
        )

    def test_str_method(self):
        borrow = Borrow.objects.get(borrow_date="2024-03-20")
        self.assertEqual(str(borrow), "Borrow 'Test' by test@example.com")
