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
        validators = [
            pleasant_xor_related,
            duration_less_than_120s,
            only_pleasant_in_related,
            pleasant_cant_have_reward_or_related,
            frequency_cant_be_less_than_weekly,
            useful_habit_must_have_schedule,
        ]


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
