from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import dateformat

from main.sitetools.backrequest import MentorRequest, StudentRequest, UserRequest, ThemeRequest, id_none


@login_required
def project_connect_page(request):
    """
    Связующая страница для прикрепления менторов к студентам
    """
    context = get_context(request, "Взаимодействие со студентами")
    template_path = 'pages/admin/project_connect.html'
    projects = None
    return render(request, template_path, context)
