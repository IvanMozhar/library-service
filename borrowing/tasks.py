from datetime import timedelta

from django.utils import timezone
from borrowing.models import Borrow
from borrowing.commands import notify


def check_overdue_borrows():

    overdue_borrows = Borrow.objects.filter(
        expected_return_date=timezone.now().date() + timedelta(days=1),
        actual_return_date__isnull=True,
    )
    for borrow in overdue_borrows:
        message = f"The following borrow is overdue: {str(borrow)}"
        notify(message)
