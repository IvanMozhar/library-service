from django.test import TestCase

from books.models import Book


class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(
            title="Test",
            author="Test Author",
            cover="Softcover",
            inventory=1,
            daily_fee=20
        )

    def test_str_method(self):
        book = Book.objects.get(title="Test")
        self.assertEqual(str(book), "Test by Test Author (Softcover)")
