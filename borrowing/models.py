from django.contrib.auth import get_user_model
from django.db import models

from books.models import Book


class Borrow(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @property
    def calculate_amount(self):
        dif = self.expected_return_date - self.borrow_date
        if 20 > dif.days >= 10:
            return self.book_id.daily_fee * 1.3
        elif 30 > dif.days >= 20:
            return self.book_id.daily_fee * 1.4
        elif dif.days >= 30:
            return self.book_id.daily_fee * 1.7
        else:
            return self.book_id.daily_fee
      
    def __str__(self):
        return f"Borrow by {self.user_id.email} at {self.borrow_date}"
