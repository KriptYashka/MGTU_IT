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


class Theme(models.Model):
    """Класс темы"""
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=64)


class Interest(models.Model):
    """Класс интереса"""
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=64)


class Student(models.Model):
    """Класс студента"""
    id = models.UUIDField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=20)
    status_pay = models.CharField(max_length=20)
    theme_id = models.UUIDField()
    mentor_id = models.UUIDField()
    interest = models.ManyToManyField(Interest)


class Mentor(models.Model):
    """Класс ментора"""
    id = models.UUIDField(primary_key=True)
    paid_student_left = models.IntegerField()
    free_student_left = models.IntegerField()
    all_student_left = models.IntegerField()
    like_student = models.ManyToManyField(Student, related_name="liked_student")
    dislike_student = models.ManyToManyField(Student, related_name="disliked_student")
    interest = models.ManyToManyField(Interest)


class Project(models.Model):
    """Класс проекта студента"""
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=100)
    img_url = models.FileField(upload_to='news/%Y/%m/')
    description = models.CharField(max_length=1000)
    post_datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.title
