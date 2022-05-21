from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    """Таблица данных пользователя. Не связана с аутентификацией."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=64)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание нового Profile, когда создается новый User"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Обновление Profile, когда обновляется User"""
    instance.profile.save()