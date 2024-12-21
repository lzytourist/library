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


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=20, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True, default=timezone.now().date)
    available_copies = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_copies > 0
