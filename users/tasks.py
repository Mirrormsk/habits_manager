from celery import shared_task
from django.conf import settings

from habits.services import TelegramService
from users.services import UserService

telegram_service = TelegramService(settings.TELEGRAM_TOKEN)
user_service = UserService()


@shared_task
def check_bot_updates():
    user_service.check_updates(telegram_service)
