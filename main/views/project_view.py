from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import dateformat

from main.forms import ThemeForm
from main.sitetools.backrequest import MentorRequest, StudentRequest, UserRequest, CategoryRequest, ThemeRequest


class Project:
    def __init__(self, name, student):
        self.name = name
        self.student = student


@login_required
def projects_page(request):
    """Страница всех проектов"""
    context = get_context(request, "Проекты")
    user_django = usertool.get_current_user(request.user.username)
    profile = user_django.profile
    user_back = UserRequest().get_by_id(profile.uid)

    status = user_back["personStatus"]
    context["status"] = status
    if status == "student":
        student = StudentRequest().get_by_id(user_back["personID"])
        theme = ThemeRequest().get_by_id(student["themeID"])
        if theme is not None:
            context['theme_name'] = theme["themeName"]

        mentor = MentorRequest().get_by_id(student["mentorID"])
        if mentor:
            fullname = "{} {} {}".format(mentor["surname"], mentor["name"], mentor["patronymic"])
            context['mentor_fullname'] = fullname

    elif status == "mentor":
        # themes = ThemeRequest().get_all()
        students = StudentRequest().get_all()
        projects = []
        for student in students:
            if student["themeID"] != "00000000-0000-0000-0000-000000000000" \
                    and student["mentorID"] == "00000000-0000-0000-0000-000000000000":
                theme = ThemeRequest().get_by_id(student["themeID"])
                project = Project(theme["themeName"], student)
                projects.append(project)

        context["projects"] = projects

    template_path = 'pages/project/projects.html'
    return render(request, template_path, context)


@login_required
def project_edit_page(request):
    """Страница создания и редактирования проекта"""
    context = get_context(request, "Проект")
    template_path = 'pages/project/project_create.html'
    # if request.user.profile.status != "student":
    #     return redirect("/projects")
    #
    # student = usertool.get_student_by_id(request.user.profile.person_id)
    # theme = usertool.get_theme_by_id(student.theme_id)
    #
    # if request.method == 'GET':
    #     context['form'] = ThemeForm
    #
    # if request.method == 'POST':
    #     template_path = 'pages/project/project_create.html'
    #     form = ThemeForm(request.POST)
    #     context['form'] = form
    #     if not (form.is_valid()):
    #         context['res'] = "Неверно введены данные"
    #         return render(request, template_path, context)
    #
    #     student = usertool.get_student_by_id(request.user.profile.person_id)
    #     theme_name = form.data["name"]
    #     if student.theme_id:
    #         theme.name = theme_name
    #         theme.save()
    #         context['res'] = "Тема обновлена."
    #     else:
    #         theme = Theme(name=theme_name)
    #         theme.save()
    #         student.theme_id = theme.id
    #         student.save()
    #         context['res'] = "Тема создана."

    # if theme is not None:
    #     context['theme_name'] = theme.name

    return render(request, template_path, context)
