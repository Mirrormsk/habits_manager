from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    pleasant_xor_related,
    duration_less_than_120s,
    only_pleasant_in_related,
    pleasant_cant_have_reward_or_related,
    frequency_cant_be_less_than_weekly,
    useful_habit_must_have_schedule,
)
from users.serializers import UserPublicSerializer


class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        pleasant_xor_related(data, self.instance)
        duration_less_than_120s(data, self.instance)
        only_pleasant_in_related(data, self.instance)
        pleasant_cant_have_reward_or_related(data, self.instance)
        frequency_cant_be_less_than_weekly(data, self.instance)
        useful_habit_must_have_schedule(data, self.instance)
        return data


class HabitPublicSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    related_habit = serializers.SlugRelatedField(
        "action",
        read_only=True,
    )

    class Meta:
        model = Habit
        fields = (
            "related_habit",
            "place",
            "action",
            "schedule",
            "is_pleasant",
            "frequency",
            "reward",
            "duration",
            "user",
        )


class HabitListSerializer(serializers.ModelSerializer):

    related_habit = serializers.SlugRelatedField(
        "action",
        read_only=True,
    )

    class Meta:
        model = Habit
        fields = (
            "id",
            "related_habit",
            "place",
            "action",
            "schedule",
            "is_pleasant",
            "frequency",
            "reward",
            "duration",
            "is_public",
        )
