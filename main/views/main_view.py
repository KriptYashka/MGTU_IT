from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import dateformat

from main.sitetools.backrequest import MentorRequest, StudentRequest, UserRequest, ThemeRequest, CategoryRequest


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
    template_path = 'pages/profile_yashka.html'
    user_django = usertool.get_current_user(request.user.username)
    profile = user_django.profile
    user_back = UserRequest().get_by_id(profile.uid)

    statuses = {
        "student": "Студент",
        "mentor": "Преподаватель",
        "admin": "Администратор",
    }

    context['email'] = user_back["email"]
    current_status = user_back["personStatus"]
    context['role'] = statuses[current_status]
    if current_status == "student":
        student = StudentRequest().get_by_id(user_back["personID"])
        if student is None:
            return render(request, 'pages/index.html', context)
        context['birthday'] = student["birthDate"][:10]
        context['full_name'] = "{} {} {}".format(student["surname"], student["name"], student["patronymic"])
        context['group'] = student["group"]
        context['description'] = student["description"]
        if student['themeID'] != "00000000-0000-0000-0000-000000000000":
            context['theme_name'] = ThemeRequest().get_by_id(student['themeID'])["themeName"]
        if student['mentorID'] != "00000000-0000-0000-0000-000000000000":
            context['user_mentor'] = MentorRequest().get_by_id(student['mentorID'])

    elif current_status == "mentor":
        mentor = MentorRequest().get_by_id(user_back["personID"])
        if mentor is None:
            return render(request, 'pages/index.html', context)
        context['birthday'] = mentor["birthDate"][:10]
        context['full_name'] = "{} {} {}".format(mentor["surname"], mentor["name"], mentor["patronymic"])
        context['description'] = mentor["description"]
        context["is_mentor"] = True

    for key in context.keys():
        if context[key] == "None":
            context[key] = None
    #  Карточка закрепленного студента/преподавателя
    return render(request, template_path, context)
