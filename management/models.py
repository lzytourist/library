from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER
    )

