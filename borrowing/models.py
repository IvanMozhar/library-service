from django.contrib.auth import get_user_model
from django.db import models

from books.models import Book


class Borrow(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="borrows")

    @property
    def calculate_amount(self):
        dif = self.expected_return_date - self.borrow_date
        price = int(self.book_id.daily_fee)
        if self.actual_return_date and self.actual_return_date > self.expected_return_date:
            return price * 2
        if 20 > dif.days >= 10:
            return price * 1.3
        elif 30 > dif.days >= 20:
            return price * 1.4
        elif dif.days >= 30:
            return price * 1.7
        else:
            return price

    def get_payment_session(self):
        return self.payments.get(borrowing=self)

    def __str__(self):
        return f"Borrow '{self.book_id.title}' by {self.user_id.email}"
