from datetime import timedelta

import requests
from django.utils import timezone
from borrowing.models import Borrow
from borrowing.commands import notify
from library_service import settings

bot_token = settings.TELEGRAM_BOT_TOKEN
chat = settings.TELEGRAM_CHAT_ID


def check_overdue_borrows():
    today = timezone.now().date()
    due_date = today + timedelta(days=1)

    overdue_borrows = Borrow.objects.filter(
        expected_return_date=due_date, actual_return_date__isnull=True
    )
    for borrow in overdue_borrows:
        message = f"The following borrow is overdue: {str(borrow)}"
        notify(message)
