from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    """Таблица данных пользователя. Не связана с аутентификацией."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    fathername = models.CharField(max_length=32)
    location = models.CharField(max_length=100)
    education_place = models.CharField(max_length=100, null=True)
    birth_date = models.DateField(null=True)