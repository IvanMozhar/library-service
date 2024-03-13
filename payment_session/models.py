from django.contrib.auth import get_user_model
from django.db import models

from borrowing.models import Borrow


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "pending"
        PAID = "PAID", "paid"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "payment"
        FINE = "FINE", "fine"

    status = models.CharField(max_length=63, choices=Status.choices)
    type = models.CharField(max_length=63, choices=Type.choices)
    session_url = models.URLField()
    session_id = models.URLField()
    borrowing = models.ForeignKey(Borrow, on_delete=models.CASCADE, related_name="payments")
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="payments")

    def __str__(self):
        return f"Payment for {str(self.borrowing)}"
