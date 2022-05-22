from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import dateformat

from main.forms import ThemeForm
from main.sitetools.backrequest import MentorRequest, StudentRequest, UserRequest, \
    CategoryRequest, ThemeRequest, id_none


class Project:
    def __init__(self, id, name, student):
        self.id = id
        self.name = name
        self.student = student


@login_required
def projects_page(request):
    """Страница всех проектов"""
    context = get_context(request, "Проекты")
    user_back = UserRequest().get_by_id(request.user.profile.uid)
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
            if student["themeID"] != id_none \
                    and student["mentorID"] == id_none:
                theme = ThemeRequest().get_by_id(student["themeID"])
                project = Project(theme["id"], theme["themeName"], student)
                projects.append(project)

        context["projects"] = projects

    template_path = 'pages/project/projects.html'
    return render(request, template_path, context)


@login_required
def project_page(request, theme_id):
    context = get_context(request, "Проект")
    user_back = UserRequest().get_by_id(request.user.profile.uid)
    theme = ThemeRequest().get_by_id(theme_id)
    if theme is None:
        return redirect("/projects")
    students = StudentRequest().get_all()
    current_student = None
    for student in students:
        if student["themeID"] == theme_id:
            current_student = student
            break
    if current_student is None:
        return redirect("/projects")
    context["student"] = current_student
    context["theme_name"] = theme["themeName"]
    if current_student["mentorID"] != id_none:
        mentor = MentorRequest().get_by_id(current_student["mentorID"])
        context["mentor"] = mentor
    template_path = "pages/project.html"
    return render(request, template_path, context)


@login_required
def project_edit_page(request):
    """Страница создания и редактирования проекта"""
    context = get_context(request, "Проект")
    template_path = 'pages/project/project_create.html'
    user_back = UserRequest().get_by_id(request.user.profile.uid)

    if user_back["personStatus"] == "mentor":
        return redirect("/projects")

    student = StudentRequest().get_by_id(user_back["personID"])
    theme = ThemeRequest().get_by_id(student["themeID"])

    if request.method == 'GET':
        context['form'] = ThemeForm

    elif request.method == 'POST':
        form = ThemeForm(request.POST)
        context['form'] = form
        if not (form.is_valid()):
            context['res'] = "Неверно введены данные"
            return render(request, template_path, context)

        theme_name = form.data["name"]
        data = {
            "id": "0",
            "themeName": theme_name,
        }
        if student["themeID"] != "00000000-0000-0000-0000-000000000000":
            data["id"] = student["themeID"]
            theme = ThemeRequest().edit(data)
            if theme is not None:
                context['res'] = "Тема обновлена."
        else:
            theme = ThemeRequest().create(data)
            if theme is not None:
                student_data = {
                    "id": student["id"],
                    "themeID": theme["id"]
                }
                StudentRequest().edit(student_data)
                context['res'] = "Тема создана."

    if theme is not None:
        context['theme_name'] = theme["themeName"]
    return render(request, template_path, context)
