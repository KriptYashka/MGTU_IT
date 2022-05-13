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
    birth_date = models.DateField(null=True)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=20)  # Студент/преподаватель/админ
    person_id = models.IntegerField(null=True)
    img = models.FileField(upload_to='user_img/%Y')


class Theme(models.Model):
    """Класс темы"""
    name = models.CharField(max_length=64)


class Interest(models.Model):
    """Класс интереса"""
    name = models.CharField(max_length=64)


class Student(models.Model):
    """Класс студента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=20)
    status_pay = models.CharField(max_length=20, null=True)
    theme_id = models.IntegerField(null=True)
    mentor_id = models.IntegerField(null=True)
    interest = models.ManyToManyField(Interest)


class Mentor(models.Model):
    """Класс ментора"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paid_student_left = models.IntegerField(default=0)
    free_student_left = models.IntegerField(default=0)
    all_student_left = models.IntegerField(default=0)
    like_student = models.ManyToManyField(Student, related_name="liked_student")
    dislike_student = models.ManyToManyField(Student, related_name="disliked_student")
    interest = models.ManyToManyField(Interest)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание нового Profile, когда создается новый User"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Обновление Profile, когда обновляется User"""
    instance.profile.save()