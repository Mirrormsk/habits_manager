from datetime import timedelta

from rest_framework import serializers


def pleasant_xor_related(habit):
    """Habit can have reward, or related habit, but only something one"""
    habit = dict(habit)
    if habit.get("reward") and habit.get("related_habit"):
        raise serializers.ValidationError(
            "Choose a related habit or a reward, but not both."
        )


def duration_less_than_120s(habit):
    """Habit duration can be only in (0, 120] seconds"""
    if not timedelta(seconds=0) < habit["duration"] <= timedelta(seconds=120):
        raise serializers.ValidationError("Duration must be positive and less than 2 min")


def only_pleasant_in_related(habit):
    """Only pleasant habit can be chosen for a related habit"""
    habit = dict(habit)
    if related := habit.get("related_habit"):
        if not related.is_pleasant:
            raise serializers.ValidationError("Only pleasant habit can be chosen for a related habit")


def pleasant_cant_have_reward_or_related(habit):
    """Pleasant habit can't have reward or related habit"""
    habit = dict(habit)
    if habit['is_pleasant'] and any([habit.get('reward'), habit.get('related_habit')]):
        raise serializers.ValidationError("Pleasant habit can't have reward or related habit")
