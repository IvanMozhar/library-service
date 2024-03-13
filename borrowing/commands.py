import requests

from library_service import settings

token = settings.TELEGRAM_BOT_TOKEN
chat_id = settings.TELEGRAM_CHAT_ID


def notify(message, bot_token=token, chat=chat_id):
    send_text = (
        f"https://api.telegram.org/bot{bot_token}/"
        f"sendMessage?chat_id={chat}&parse_mode=Markdown&text={message}"
    )
    requests.post(send_text)
