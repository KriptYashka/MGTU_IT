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
    description = models.CharField(max_length=1000)


class Mentor(models.Model):
    id = models.IntegerField(primary_key=True)
    # status = models.ManyToOneRel()


class Project(models.Model):
    title = models.CharField(max_length=100)
    img_url = models.FileField(upload_to='news/%Y/%m/')
    description = models.CharField(max_length=1000)
    post_datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.title