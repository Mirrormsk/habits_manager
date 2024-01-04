from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import (
    HabitListSerializer,
    HabitPublicSerializer,
    HabitCreateSerializer,
)


class HabitViewSet(ModelViewSet):

    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Habit.objects.all()

        return Habit.objects.filter(user=user)

    @action(detail=False, methods=["get"])
    def public(self, request, pk=None):
        queryset = Habit.objects.filter(is_public=True)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitPublicSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_permissions(self):
        match self.action:  # noqa
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

    def get_serializer_class(self):
        match self.action:  # noqa
            case "create" | "update" | "partial_update":
                return HabitCreateSerializer
            case "list" | "retrieve":
                return HabitListSerializer


