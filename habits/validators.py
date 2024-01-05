from datetime import timedelta

from rest_framework import serializers

from habits.models import Habit


def pleasant_xor_related(value, instance: Habit):
    """Habit can have reward, or related habit, but only something one"""
    if "is_pleasant" in value.keys():
        is_pleasant = value["is_pleasant"]
    else:
        is_pleasant = instance.is_pleasant

    if "reward" in value.keys():
        reward = value["reward"]
    else:
        if instance:
            reward = instance.reward
        else:
            reward = None

    if "related_habit" in value.keys():
        related_habit = value["related_habit"]
    else:
        if instance:
            related_habit = instance.related_habit
        else:
            related_habit = None

    if not is_pleasant and not bool(reward) ^ bool(related_habit):
        raise serializers.ValidationError(
            "Choose a related habit or a reward, but not both."
        )


def duration_less_than_120s(value, instance: Habit):
    """Habit duration can be only in (0, 120] seconds"""
    value = dict(value)
    if "duration" in value.keys():
        duration = value["duration"]
    else:
        duration = instance.duration

    if not timedelta(seconds=0) < duration <= timedelta(seconds=120):
        raise serializers.ValidationError(
            "Duration must be positive and less than 2 min"
        )


def only_pleasant_in_related(value, instance: Habit):
    """Only pleasant habit can be chosen for a related habit"""
    value = dict(value)
    if "related_habit" in value.keys():
        related_habit = value["related_habit"]
    else:
        if instance:
            related_habit = instance.related_habit
        else:
            related_habit = None

    if related_habit:
        if not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Only pleasant habit can be chosen for a related habit"
            )


def pleasant_cant_have_reward_or_related(value, instance: Habit):
    """Pleasant habit can't have reward or related habit"""
    value = dict(value)

    if "is_pleasant" in value.keys():
        is_pleasant = value["is_pleasant"]
    else:
        is_pleasant = instance.is_pleasant
    if "reward" in value.keys():
        reward = value["reward"]
    else:
        if instance:
            reward = instance.reward
        else:
            reward = None
    if "related_habit" in value.keys():
        related_habit = value["related_habit"]
    else:
        if instance:
            related_habit = instance.related_habit
        else:
            related_habit = None

    if is_pleasant and any([reward, related_habit]):
        raise serializers.ValidationError(
            "Pleasant habit can't have reward or related habit"
        )


def frequency_cant_be_less_than_weekly(value, instance: Habit):
    """You can't make a habit less than once every 7 days."""
    value = dict(value)
    if "frequency" in value.keys():
        frequency = value["frequency"]
    else:
        frequency = instance.frequency

    if frequency > 7:
        raise serializers.ValidationError(
            "You can't make a habit less than once every 7 days"
        )


def useful_habit_must_have_schedule(value, instance: Habit):
    """Useful habit must have a schedule"""
    value = dict(value)
    if "is_pleasant" in value.keys():
        is_pleasant = value["is_pleasant"]
    else:
        is_pleasant = instance.is_pleasant
    if "schedule" in value.keys():
        schedule = value["schedule"]
    else:
        if instance:
            schedule = instance.schedule
        else:
            schedule = None

    if not is_pleasant and not schedule:
        raise serializers.ValidationError("Useful habit must have a schedule")
