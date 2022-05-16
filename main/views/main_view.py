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


@login_required
def profile_page(request):
    """Страница профиля"""
    context = get_context(request, "Профиль")
    user = usertool.get_current_user(request.user.username)
    profile = user.profile
    context['email'] = user.email
    context['birthday'] = profile.birth_date
    context['full_name'] = "{} {} {}".format(profile.surname, profile.name, profile.fathername)

    statuses = {
        "student": "Студент",
        "mentor": "Преподаватель",
        "admin": "Администратор",
    }

    desc = "Программист, 20 лет, стаж 4 года работы. Портфолио - РУДН, ШП."
    context['description'] = desc
    context['role'] = statuses[profile.status]
    context['group'] = "СГН3-41Б"
    if profile.status == "student":
        current_student = usertool.get_student_by_id(profile.person_id)
        print(current_student)
    elif profile.status == "mentor":
        current_mentor = usertool.get_mentor_by_id(profile.person_id)
        print(current_mentor)
    else:
        pass

    template_path = 'pages/profile_yashka.html'
    return render(request, template_path, context)
