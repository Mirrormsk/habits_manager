from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.main_url = "/habits/"
        self.detail_url = "/habits/{}/"
        self.public_url = "/habits/public/"
        self.user_1 = User.objects.create(
            email="test@test.com", password="Password1234"
        )
        self.superuser = User.objects.create(
            email="admin@test.com",
            password="Password1234",
            is_superuser=True,
            is_staff=True,
        )
        self.habit_1 = Habit.objects.create(
            user=self.user_1,
            place="test place",
            action="test action",
            schedule="21:00:00",
            is_pleasant=False,
            frequency=1,
            reward="test reward",
            duration="00:00:20",
            is_public=False,
        )

    def test_create_habit(self):
        data = {
            "place": "test place",
            "action": "test action",
            "schedule": "21:00:00",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "test reward",
            "duration": "00:00:20",
            "is_public": False,
            # "related_habit": 23,
        }

        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(self.main_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_habits_list(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_habits_detail(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(self.detail_url.format(self.habit_1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.habit_1.id)
        self.assertEqual(response.data["action"], self.habit_1.action)

    def test_list_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_public_habits(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(self.public_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

        public_habit_data = {
            "place": "test place",
            "action": "test action",
            "schedule": "21:00:00",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "test reward",
            "duration": "00:00:20",
            "is_public": True,
            # "related_habit": 23,
        }

        self.client.post(self.main_url, public_habit_data, format="json")
        response = self.client.get(self.public_url)
        self.assertEqual(response.data["count"], 1)

    def test_update_habit(self):
        self.client.force_authenticate(user=self.user_1)

        patch_data = {"place": "new test place"}

        response = self.client.patch(
            self.detail_url.format(self.habit_1.id), patch_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_habit(self):
        self.client.force_authenticate(user=self.user_1)
        list_response = self.client.get(self.main_url)
        self.assertEqual(list_response.data["count"], 1)
        response = self.client.delete(
            self.detail_url.format(list_response.data["results"][0]["id"])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_validate_pleasant_xor_related(self):
        self.client.force_authenticate(user=self.user_1)
        data = {
            "place": "test place",
            "action": "test action",
            "schedule": "21:00:00",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "test reward",
            "duration": "00:00:20",
            "is_public": True,
            "related_habit": self.habit_1.id,
        }
        response = self.client.post(self.main_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duration_less_than_120s(self):
        self.client.force_authenticate(user=self.user_1)
        patch_data = {"duration": "10:00:00"}
        response = self.client.patch(
            self.detail_url.format(self.habit_1.id), patch_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
