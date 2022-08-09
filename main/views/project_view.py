from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import dateformat

from main.forms import ThemeForm
from main.sitetools.backrequest import MentorRequest, StudentRequest, UserRequest, ThemeRequest, id_none, \
    ModelRequestUser, ModelRequestStudent, ModelRequestTheme, ModelRequestMentor
from main.sitetools.project import Project, create_event, get_all_projects, get_student_by_theme_id


@login_required
def projects_page(request):
    """
    Страница всех проектов для преподавателя
    Страница своего проекта для студента
    """
    context = get_context(request, "Проекты")
    user_back = ModelRequestUser(request.user.profile.uid)
    context["status"] = user_back.person_status

    if user_back.person_status == "student":
        student = ModelRequestStudent(user_back.person_id)

        # Вывод темы
        theme = ModelRequestTheme(student.theme_id)
        if theme:
            context['theme_name'] = theme.name

        # Вывод ментора
        mentor = ModelRequestMentor(student.mentor_id)
        if mentor:
            context['mentor_fullname'] = mentor.fullname
            context['has_mentor'] = True

    elif user_back.person_status == "mentor":
        projects = get_all_projects()
        my_projects, other_projects = [], []
        for project in projects:
            if project.student["mentorID"] == user_back.person_id:
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
    """
    Страница одного проекта
    TODO: Разбить на функции
    """
    context = get_context(request, "Проект")
    user = ModelRequestUser(request.user.profile.uid)
    context["user_back"] = user
    theme = ModelRequestTheme(theme_id)
    if not theme:
        return redirect("/projects")

    # Поиск студента темы
    student = get_student_by_theme_id(theme_id)
    if student is None:
        return redirect("/projects")

    # Заполнение данных: ФИО, дата рождения
    student.fullname = f'{student.surname} {student.name} {student.patronymic}'
    student.birthdate = student.birthdate[:10]
    context["student"] = student
    context["theme_name"] = theme.name

    is_free = student.status_pay == "free"
    is_paid = student.status_pay == "paid"
    #  Запрос на прикрепление студента
    if request.method == "POST" and user.person_status == "mentor":
        type_request = request.POST.get("type_request")
        if type_request == "ADD":
            # Распределение слотов ментора
            mentor = ModelRequestMentor(user.person_id)
            is_record = True
            if is_free and mentor.free_students_left > 0:
                mentor.free_students_left -= 1
            elif is_paid and mentor.paid_students_left > 0:
                mentor.paid_students_left -= 1
            elif mentor.all_students_left > 0:
                mentor.all_students_left -= 1
            else:
                is_record = False

            if is_record:
                student.mentor_id = mentor.id
                student.edit()
                mentor.edit()
                # create_event(current_student, mentor, theme.name)
        elif type_request == "DEL":
            # Удаление связи ментора и студента
            mentor = ModelRequestMentor(user.person_id)
            student.mentor_id = id_none
            student.edit()
            if mentor.all_students_left == -1:
                if is_paid:
                    mentor.paid_students_left += 1
                elif is_free:
                    mentor.free_students_left += 1
            else:
                mentor.all_students_left += 1
                mentor.edit()

            return redirect("/projects")

    #  Настройка кнопок на шаблоне для преподавателя
    if user.person_status == "mentor":
        mentor = ModelRequestMentor(user.person_id)
        # Если проект уже составлен
        if student.mentor_id != id_none:
            context["disable_add_project"] = True
            context["register_btn_value"] = "Вы участвуете" if mentor.id == user.person_id else "Проект составлен"
        # Если проект не составлен и есть свободные места
        elif is_free and mentor.free_students_left > 0 or is_paid \
                and mentor.paid_students_left > 0 or mentor.all_students_left > 0:
            context["register_btn_value"] = "Начать работу со студентом"
        # Если проект не составлен и нет свободных мест
        else:
            context["disable_add_project"] = True
            context["register_btn_value"] = "У вас не хватает мест"

    if student.mentor_id != id_none:
        mentor = ModelRequestMentor(student.mentor_id)
        context["mentor"] = mentor

    template_path = "pages/project/project.html"
    return render(request, template_path, context)


@login_required
def project_edit_page(request):
    """
    Страница создания и редактирования проекта
    """
    context = get_context(request, "Проект")
    template_path = 'pages/project/project_create.html'
    user = ModelRequestUser(request.user.profile.uid)

    if user.person_status == "mentor":
        return redirect("/projects")

    student = ModelRequestStudent(user.person_id)

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
        theme = ModelRequestTheme(data)
        if student.theme_id != id_none:
            theme.id = student.theme_id
            theme.edit()
            if theme:
                context['res'] = "Тема обновлена."
        else:
            if theme:
                student.theme_id = theme.id
                student.edit()
                context['res'] = "Тема создана."

    theme = ModelRequestTheme(student.theme_id)
    if theme:
        context['theme_name'] = theme.name
    return render(request, template_path, context)
