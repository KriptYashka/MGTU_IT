from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import dateformat

from main.sitetools.backrequest import UserRequest, StudentRequest, MentorRequest, ThemeRequest, id_none, \
    ModelRequestUser, ModelRequestStudent, ModelRequestMentor, ModelRequestTheme
from main.sitetools.backrequest import get_user_by_person


def get_attached_user_students(mentor_id: str) -> dict[ModelRequestUser, ModelRequestStudent]:
    """
    Возвращает словарь пользователей-студентов, прикрепленных к ментору

    :param mentor_id: ID ментора
    :return: Словарь пользователей-студентов, прикрепленных к ментору
    """
    students_dict = StudentRequest().get_all()
    attached_user_student = {}
    attached_students_ids = []
    for student_dict in students_dict:
        if student_dict["mentorID"] == mentor_id:
            attached_students_ids.append(student_dict["id"])

    users_dict = UserRequest().get_all()

    for user_dict in users_dict:
        if user_dict["personID"] in attached_students_ids:
            user = ModelRequestUser().load_data_dict(user_dict)
            # Требуется использовать ранее полученную информацию, иначе много вызовов
            student = ModelRequestStudent(user.person_id)
            # ------------------------------------------------------------------
            attached_user_student[user] = student

    return attached_user_student


def get_profile_student_context(context: dict, student: ModelRequestStudent, user: ModelRequestUser) -> dict:
    context['student'] = student
    context['student_user'] = user
    if student.theme_id != id_none:
        theme = ModelRequestTheme(student.theme_id)
        context['theme_name'] = theme.name
    if student.mentor_id != id_none:
        mentor = ModelRequestMentor(student.mentor_id)
        mentor_user = get_user_by_person(mentor.id)
        context['mentor'] = mentor
        context['mentor_user'] = mentor_user
    return context


def get_profile_mentor_context(context: dict, mentor: ModelRequestMentor) -> dict:
    context["mentor"] = mentor
    attached_user_students = get_attached_user_students(mentor.id)
    paid_students, free_students = 0, 0
    for user, student in attached_user_students.items():
        if student.theme_id != id_none:
            attached_user_students[user].theme_name = ModelRequestTheme(student.theme_id).name
        if student.status_pay == "free":
            free_students += 1
        elif student.status_pay == "paid":
            paid_students += 1
    if attached_user_students:
        context["attached_user_students"] = attached_user_students

    context["paid_students_left"] = mentor.paid_students_left
    if paid_students > 0:
        context["paid_students"] = paid_students
    context["free_students_left"] = mentor.free_students_left
    if free_students > 0:
        context["free_students"] = free_students

    context["all_students_left"] = mentor.all_students_left
    count_all_slot = mentor.all_students_left + mentor.paid_students_left + mentor.free_students_left + \
                     len(attached_user_students)
    if count_all_slot:
        context["paid_students_width"] = paid_students / count_all_slot * 100
        context["free_students_width"] = free_students / count_all_slot * 100

    # context["all_students_width"] = free_students / count_all_slot * 100
    context["student_count"] = mentor.all_students_left + paid_students + free_students

    return context


# Страницы


def index_page(request):
    """
    Главная страница
    """
    context = get_context(request, "Главная", False)
    template_path = 'pages/index.html'

    count_mentor = len(MentorRequest().get_all())
    count_student = len(StudentRequest().get_all())
    context["count_all"] = count_mentor + count_student
    context["count_mentor"] = count_mentor
    context["count_student"] = count_student
    return render(request, template_path, context)


def about_page(request):
    """
    Страница информации о сайте
    """
    context = get_context(request, "О проекте")
    template_path = 'pages/about.html'

    return render(request, template_path, context)


@login_required
def profile_page(request):
    """
    Страница профиля для просмотра информации
    """
    context = get_context(request, "Профиль")
    template_path = 'pages/index.html'

    user = ModelRequestUser(request.user.profile.uid)
    context["user"] = user

    statuses = {
        "student": "Студент",
        "mentor": "Преподаватель",
        "admin": "Администратор",
    }
    current_status = "unknown"

    if user.person_status:
        current_status = user.person_status
        context['role'] = statuses[current_status]

    if current_status == "student":
        student = ModelRequestStudent(user.person_id)
        if not student:
            return render(request, template_path, context)
        context = get_profile_student_context(context, student, user)
        template_path = 'pages/profile_student.html'

    elif current_status == "mentor":
        mentor = ModelRequestMentor(user.person_id)
        if not mentor:
            return render(request, template_path, context)
        context = get_profile_mentor_context(context, mentor)
        template_path = 'pages/profile_mentor.html'

    return render(request, template_path, context)


@login_required
def edit_profile_page(request):
    """
    Страница редактирования профиля
    """
    context = get_context(request, "Редактирование")
    template_path = 'pages/profile_edit.html'

    return render(request, template_path, context)
