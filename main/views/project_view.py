from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import dateformat

from main.forms import ThemeForm
from main.sitetools.backrequest import MentorRequest, StudentRequest, UserRequest, \
    CategoryRequest, ThemeRequest, EventRequest, id_none


class Project:
    def __init__(self, id, name, student):
        self.id = id
        self.name = name
        self.student = student


def create_event(student, mentor, theme_name):
    data_event = {
        "id": "0",

        "nameS": student["name"],
        "surnameS": student["surname"],
        "patronymicS": student["patronymic"],
        "birthDateS": student["birthDate"],
        "groupS": student["group"],

        "nameM": mentor["name"],
        "surnameM": mentor["surname"],
        "patronymicM": mentor["patronymic"],
        "birthDateM": mentor["birthDate"],

        "categoryNameID": id_none,
        "categoryName": None,
        "themeName": theme_name
    }
    EventRequest().create(data_event)


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
        students = StudentRequest().get_all()
        my_projects = []
        other_projects = []
        for student in students:
            if student["themeID"] != id_none \
                    and student["mentorID"] == id_none:
                theme = ThemeRequest().get_by_id(student["themeID"])
                project = Project(theme["id"], theme["themeName"], student)
                if student["mentorID"] == user_back["id"]:
                    my_projects.append(project)
                else:
                    other_projects.append(project)
        context["my_projects"] = my_projects
        context["projects"] = other_projects

    template_path = 'pages/project/projects.html'
    return render(request, template_path, context)


# http://127.0.0.1:8000/project/b53b0c2b-4c5f-456b-85b9-c33976b6fed0
@login_required
def project_page(request, theme_id):
    context = get_context(request, "Проект")
    user_back = UserRequest().get_by_id(request.user.profile.uid)
    context["user_back"] = user_back
    theme = ThemeRequest().get_by_id(theme_id)
    if theme is None:
        return redirect("/projects")

    # Поиск студента темы
    students = StudentRequest().get_all()
    current_student = None
    for student in students:
        if student["themeID"] == theme_id:
            current_student = student
            break
    if current_student is None:
        return redirect("/projects")

    # Заполнение данных: ФИО, дата рождения
    current_student["full_name"] = "{} {} {}".format(current_student["surname"], current_student["name"],
                                                     current_student["patronymic"])
    current_student["birthDate"] = current_student["birthDate"][:10]
    is_free = current_student["statusPay"] == "free"
    is_pay = current_student["statusPay"] == "pay"
    # Заполнение данных: платная или бюджетная основа
    if is_free == "free":
        current_student["status_pay"] = "Бюджет"
    elif is_pay == "pay":
        current_student["status_pay"] = "Платная основа"
    else:
        current_student["status_pay"] = "Не указано"

    context["student"] = current_student
    context["theme_name"] = theme["themeName"]

    if request.method == "POST" and user_back["personStatus"] == "mentor":
        # Распределение в нужную категорию
        mentor = MentorRequest().get_by_id(user_back["personID"])
        is_record = True
        if is_free and mentor["freeStudentsLeft"] > 0:
            mentor["freeStudentsLeft"] -= 1
        elif is_pay and mentor["paidStudentsLeft"] > 0:
            mentor["paidStudentsLeft"] -= 1
        elif mentor["allStudentsLeft"] > 0:
            mentor["allStudentsLeft"] -= 1
        else:
            is_record = False

        if is_record:
            MentorRequest().edit(mentor)
            current_student["mentorID"] = mentor["id"]
            StudentRequest().edit(current_student)
            create_event(current_student, mentor, theme["themeName"])

    if user_back["personStatus"] == "mentor":
        mentor = MentorRequest().get_by_id(user_back["personID"])
        # Если проект уже составлен
        if current_student["mentorID"] != id_none:
            context["disable"] = True
            context["register_btn_value"] = \
                "Вы участвуете" if mentor["id"] == user_back["personID"] else "Проект составлен"
        # Если проект не составлен и есть свободные места
        elif is_free and mentor["freeStudentsLeft"] > 0 or is_pay and mentor["paidStudentsLeft"] > 0 or mentor["allStudentsLeft"] > 0:
            context["register_btn_value"] = "Начать работу со студентом"
        # Если проект не составлен и нет свободных мест
        else:
            context["disable"] = True
            context["register_btn_value"] = "У вас не хватает мест"

    if current_student["mentorID"] != id_none:
        mentor = MentorRequest().get_by_id(current_student["mentorID"])
        context["mentor"] = mentor

    template_path = "pages/project/project.html"
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
            cod = ThemeRequest().edit(data)
            if cod is not None:
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
        context['theme_name'] = str(theme["themeName"])
    return render(request, template_path, context)
