from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'chat_id', 'tg_invite_link', "city"]
        read_only_fields = ["id", "tg_invite_link"]

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.
        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class UserPublicSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()

    @staticmethod
    def get_first_name(obj):
        return obj.first_name if obj.first_name else "Anonymous"

    class Meta:
        model = User
        fields = ("first_name", 'pk')
