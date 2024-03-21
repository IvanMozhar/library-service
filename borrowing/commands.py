import requests

from library_service import settings


def notify(
    message, bot_token=settings.TELEGRAM_BOT_TOKEN, chat=settings.TELEGRAM_CHAT_ID
):
    send_text = (
        f"https://api.telegram.org/bot{bot_token}/"
        f"sendMessage?chat_id={chat}&parse_mode=Markdown&text={message}"
    )
    requests.post(send_text)
