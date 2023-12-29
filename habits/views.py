from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


