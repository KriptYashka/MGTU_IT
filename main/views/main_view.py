from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import dateformat


def index_page(request):
    """Главная страница"""
    context = get_context(request, "Главная", False)
    template_path = 'pages/index.html'
    return render(request, template_path, context)


def about_page(request):
    """Страница информации о сайте"""
    context = get_context(request, "О проекте")
    template_path = 'pages/about.html'
    return render(request, template_path, context)


def get_context_student(context: dict, user):
    profile = user.profile
    current_student = usertool.get_student_by_id(profile.person_id)

    context['group'] = current_student.group
    # context['description'] = profile.description
    context['description'] = "Программист, 20 лет, стаж 4 года работы. Портфолио - РУДН, ШП."
    theme = usertool.get_theme_by_id(current_student.theme_id)
    if theme:
        context['theme'] = theme
    user, profile = usertool.get_user_by_mentor_id(current_student.mentor_id)
    context['user_mentor'] = user
    return context


@login_required
def profile_page(request):
    """Страница профиля"""
    context = get_context(request, "Профиль")
    user = usertool.get_current_user(request.user.username)
    profile = user.profile
    context['email'] = user.email
    context['birthday'] = profile.birth_date  # По логике бека должен уйти в if-else
    context['full_name'] = "{} {} {}".format(profile.surname, profile.name, profile.fathername)

    statuses = {
        "student": "Студент",
        "mentor": "Преподаватель",
        "admin": "Администратор",
    }

    context['role'] = statuses[profile.status]
    if profile.status == "student":
        context = get_context_student(context, user)
        template_path = 'pages/profile_yashka.html'
    elif profile.status == "mentor":
        current_mentor = usertool.get_mentor_by_id(profile.person_id)
        context["is_mentor"] = True
        template_path = 'pages/profile_yashka.html'
    else:
        template_path = 'pages/profile_yashka.html'

    #  Карточка закрепленного студента/преподавателя
    return render(request, template_path, context)
