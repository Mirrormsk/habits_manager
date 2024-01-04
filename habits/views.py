from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitPublicSerializer


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    @action(detail=False, methods=["get"])
    def public(self, request, pk=None):
        queryset = Habit.objects.filter(is_public=True)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitPublicSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_permissions(self):
        match self.action:
            case "public":
                permission_classes = [IsAuthenticated]
            case "list" | "retrieve":
                permission_classes = [IsAuthenticated, IsOwner]
            case "create":
                permission_classes = [IsAuthenticated]
            case "update" | "partial_update":
                permission_classes = [IsAuthenticated, IsOwner]
            case "destroy":
                permission_classes = [IsAuthenticated, IsOwner]
            case _:
                permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
