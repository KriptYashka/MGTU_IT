from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import dateformat

from main.forms import ThemeForm
from main.models import Theme


class Project:
    def __init__(self, name, prof_stud):
        self.name = name
        self.prof_stud = prof_stud


@login_required
def projects_page(request):
    """Страница всех проектов"""
    context = get_context(request, "Проекты")
    context["user"] = request.user

    if request.user.profile.status == "student":
        student = usertool.get_student_by_id(request.user.profile.person_id)
        theme = usertool.get_theme_by_id(student.theme_id)
        if theme is not None:
            context['theme_name'] = theme.name

        if student.mentor_id:
            mentor = usertool.get_mentor_by_id(student.mentor_id)
            fullname = f"{mentor.user.profile.surname} {mentor.user.profile.name} {mentor.user.profile.fathername}"
            context['mentor_fullname'] = fullname

    elif request.user.profile.status == "mentor":
        themes = Theme.objects.all()
        projects = []
        for theme in themes:
            student = usertool.get_student_by_theme_id(theme.id)
            if not student.mentor_id:
                project = Project(theme.name, student.user.profile)
                projects.append(project)

        context["projects"] = projects

    template_path = 'pages/project/projects.html'
    return render(request, template_path, context)


@login_required
def project_edit_page(request):
    """Страница создания и редактирования проекта"""
    context = get_context(request, "Проект")
    template_path = 'pages/project/project_create.html'
    if request.user.profile.status != "student":
        return redirect("/projects")

    student = usertool.get_student_by_id(request.user.profile.person_id)
    theme = usertool.get_theme_by_id(student.theme_id)

    if request.method == 'GET':
        context['form'] = ThemeForm

    if request.method == 'POST':
        template_path = 'pages/project/project_create.html'
        form = ThemeForm(request.POST)
        context['form'] = form
        if not (form.is_valid()):
            context['res'] = "Неверно введены данные"
            return render(request, template_path, context)

        student = usertool.get_student_by_id(request.user.profile.person_id)
        theme_name = form.data["name"]
        if student.theme_id:
            theme.name = theme_name
            theme.save()
            context['res'] = "Тема обновлена."
        else:
            theme = Theme(name=theme_name)
            theme.save()
            student.theme_id = theme.id
            student.save()
            context['res'] = "Тема создана."

    if theme is not None:
        context['theme_name'] = theme.name

    return render(request, template_path, context)
