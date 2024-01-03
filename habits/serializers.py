from rest_framework import serializers

from habits.models import Habit
from habits.validators import pleasant_xor_related


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [pleasant_xor_related]

