import datetime

from django.conf import settings
import logging

from habits.models import Habit
from habits.services import TelegramService
from users.models import User
import base64

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self):
        self.secret_separator = "#"

    @staticmethod
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_user_by_pk(pk: int):
        return User.objects.filter(id=pk).first()

    def generate_invite(self, user: User, telegram_service: TelegramService) -> str:
        secret_text = f"{user.id}{self.secret_separator}{user.uid}"
        secret = base64.b64encode(secret_text.encode("utf-8")).decode("utf-8")
        return telegram_service.generate_invite_link(secret)

    @staticmethod
    def decode_string(encoded_string: str) -> str:
        decoded = base64.b64decode(encoded_string).decode("utf-8")
        return decoded

    @staticmethod
    def is_user_data_correct(user_id: int, uid: str) -> tuple[bool, User | None]:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False, None
        else:
            if uid == str(user.uid):
                return True, user
            else:
                return False, None

    def process_invite_update(self, update: dict, telegram_service: TelegramService):
        text = update["message"]["text"]
        if text.startswith("/start"):
            command, *secret = text.split(maxsplit=1)
            if secret:
                try:
                    decoded_secret = base64.b64decode(secret[0]).decode("utf-8")
                    pk, uid = decoded_secret.split(self.secret_separator)
                    data_correct, user = self.is_user_data_correct(pk, uid)
                    if data_correct:
                        user.chat_id = update["message"]["chat"]["id"]
                        user.save()

                        telegram_service.send_message(
                            chat_id=user.chat_id,
                            text=f"Ваш Telegram-аккаунт успешно привязан к учетной записи {user.email}",
                        )

                except Exception as ex:
                    logger.exception(ex)

    def check_updates(self, telegram_service: TelegramService):

        updates = telegram_service.get_updates()
        for update in updates:
            if "message" in update.keys():
                self.process_invite_update(update, telegram_service)

    @staticmethod
    def send_habits_notification(telegram_service: TelegramService):
        users = User.objects.all()
        tz_info = datetime.timezone(datetime.timedelta(hours=3))
        for user in users:
            if user.chat_id:
                now = datetime.datetime.now(tz_info)
                user_habits = Habit.objects.filter(user=user)
                for habit in user_habits:

                    if (
                        not habit.last_sent
                        or now - habit.last_sent
                        >= datetime.timedelta(days=habit.frequency)
                    ):
                        if (not habit.is_pleasant) and habit.schedule <= now.time():
                            telegram_service.send_message(
                                text=f"Напоминание о привычке:\n"
                                f"Действие: {habit.action}\n"
                                f"Место: {habit.place}\n"
                                f"Время: {habit.schedule}\n"
                                f"Награда: {habit.reward if habit.reward else habit.related_habit.action}",
                                chat_id=user.chat_id,
                            )
                            habit.last_sent = now
                            habit.save()
