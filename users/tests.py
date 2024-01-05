from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from habits.services import TelegramService
from users.models import User
from users.services import UserService


class UsersTestCase(APITestCase):
    def setUp(self) -> None:
        self.test_chat_id = 146850962
        self.main_url = "/users/"
        self.detail_url = "/users/{}/"
        self.user_1 = User.objects.create(
            email="test@test.com", password="Password1234"
        )
        self.telegram_service = TelegramService(settings.TELEGRAM_TOKEN)
        self.user_service = UserService()

    def test_user_creation(self):
        user_data = {"email": "test@testing1.com", "password": "1234556"}
        response = self.client.post(self.main_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_himself(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(self.detail_url.format(str(self.user_1.id)))
        self.assertIn("tg_invite_link", response.data)

    def test_user_service_get_by_email(self):
        user = UserService.get_user_by_email(self.user_1.email)
        self.assertEqual(user, self.user_1)

    def test_user_service_get_by_pk(self):
        user = UserService.get_user_by_pk(self.user_1.pk)
        self.assertEqual(user, self.user_1)

    def test_user_service_process_invite(self):
        invite_link = self.user_service.generate_invite(
            self.user_1, self.telegram_service
        )

        invite_update_message_text = invite_link.lstrip(
            f"https://t.me/{self.telegram_service.username}?"
        )

        update_body = {
            "message": {
                "text": f"/start {invite_update_message_text}",
                "chat": {"id": self.test_chat_id},
            }
        }

        self.user_service.process_invite_update(
            update_body, telegram_service=self.telegram_service
        )

    def test_users_list(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
