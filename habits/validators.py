from rest_framework import serializers


def pleasant_xor_related(habit):
    if not bool(habit['reward']) ^ (habit['related_habit'] is not None):
        raise serializers.ValidationError('Choose a related habit or a reward, but not both.')