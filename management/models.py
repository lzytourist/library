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
    published_date = models.DateField(null=True, blank=True)
    available_copies = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_copies > 0


class Borrow(models.Model):
    class Status(models.TextChoices):
        BORROWED = 'borrowed', 'Borrowed'
        RETURNED = 'returned', 'Returned'

    member = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='borrowed'
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.BORROWED)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)


class Fine(models.Model):
    class Status(models.TextChoices):
        PAID = 'paid', 'Paid'
        UNPAID = 'unpaid', 'Unpaid'

    member = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        related_name='overdue_fine_transactions'
    )
    borrow = models.ForeignKey(
        to=Borrow,
        on_delete=models.PROTECT,
        related_name='overdue_fine_transactions'
    )
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UNPAID)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
