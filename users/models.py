import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    chat_id = models.PositiveIntegerField(verbose_name='telegram chat id', **NULLABLE)
    tg_invite_link = models.URLField(**NULLABLE, verbose_name='telegram invite')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
