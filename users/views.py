from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.permissions import IsProfileOwnerOrReadOnly
from users.serializers import UserSerializer, UserPublicSerializer

from users.tasks import telegram_service, user_service


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]
    lookup_field = 'pk'

    def perform_create(self, serializer):
        user = serializer.save()
        telegram_invite_link = user_service.generate_invite(user, telegram_service)
        user.tg_invite_link = telegram_invite_link
        user.save()

    def get_serializer_class(self):

        if self.action == "retrieve":
            user = self.request.user
            instance = self.get_object()
            if instance == user:
                return UserSerializer
            return UserPublicSerializer

        elif self.action == "list":
            return UserPublicSerializer

        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return UserSerializer

    def get_permissions(self):
        match self.action:
            case "create":
                permission_classes = [AllowAny]
            case _:
                permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
