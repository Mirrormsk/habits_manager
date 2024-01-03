from datetime import timedelta

from rest_framework import serializers


def pleasant_xor_related(habit):
    """Habit can have reward, or related habit, but only something one"""
    if bool(habit["reward"]) & (habit["related_habit"] is not None):
        raise serializers.ValidationError(
            "Choose a related habit or a reward, but not both."
        )


def duration_less_than_120s(habit):
    """Habit duration can be only in (0, 120] seconds"""
    if not timedelta(seconds=0) < habit["duration"] <= timedelta(seconds=120):
        raise serializers.ValidationError("Duration must be positive and less than 2 min")

