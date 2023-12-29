from django.shortcuts import render

from rest_framework.viewsets import ViewSet

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitViewSet(ViewSet):
    model = Habit
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


