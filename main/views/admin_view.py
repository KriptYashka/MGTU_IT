from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import dateformat
from main.sitetools.project import get_all_projects, get_all_mentors, get_student_by_theme_id

from main.sitetools.backrequest import MentorRequest, StudentRequest, UserRequest, ThemeRequest, id_none


@login_required
def project_connect_page(request):
    """
    Связующая страница для прикрепления менторов к студентам
    """
    context = get_context(request, "Взаимодействие со студентами")
    template_path = 'pages/admin/project_connect.html'
    mentors = get_all_mentors()
    free_mentors, closed_mentors = [], []
    for mentor in mentors:
        free_mentors.append(mentor) if mentor.is_has_slot() else closed_mentors.append(mentor)
    context["free_mentors"] = free_mentors
    context["closed_mentors"] = closed_mentors
    projects = get_all_projects()
    return render(request, template_path, context)
