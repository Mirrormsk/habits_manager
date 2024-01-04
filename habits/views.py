from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Public habits list",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "first_name": openapi.Schema(
                                    type=openapi.TYPE_STRING, description="User name"
                                ),
                                "pk": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description="User pk"
                                ),
                            },
                        ),
                        "related_habit": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Related habit action"
                        ),
                        "place": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Habit action place"
                        ),
                        "action": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Habit action"
                        ),
                        "schedule": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Habit schedule time"
                        ),
                        "is_pleasant": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, description="Is habit a pleasant"
                        ),
                        "frequency": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Habit frequency in days"
                        ),
                        "reward": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Habit reward"
                        ),
                        "duration": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Habit duration"
                        )},
                ),
            ),
        },
    )
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
