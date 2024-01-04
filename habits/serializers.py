from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    pleasant_xor_related,
    duration_less_than_120s,
    only_pleasant_in_related, pleasant_cant_have_reward_or_related,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            pleasant_xor_related,
            duration_less_than_120s,
            only_pleasant_in_related,
            pleasant_cant_have_reward_or_related,
        ]
