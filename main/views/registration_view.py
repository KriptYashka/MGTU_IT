import datetime
import re

from main.forms import RegistrationForm, LoginForm

from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from main.sitetools import usertool
from main.sitetools.texttool import get_context

from sitetools.backrequest import UserRequest, MentorRequest, StudentRequest


def register_student(data):
    student_data = {
        "id": "0",
        "name": data["name"],
        "surname": data["surname"],
        "patronymic": data["fathername"],
        "birthdate": f"{data['birth_day']}.{data['birth_month']}.{data['birth_year']}",
        "Group": data['group'],
        "Mentorid": "00000000-0000-0000-0000-000000000000",
        "Themeid": "00000000-0000-0000-0000-000000000000"
    }
    student = StudentRequest().create(student_data)
    if student["id"] is None:
        return None

    user_data = {
        "id": "0",
        "login": data["login"],
        "password": data["password"],
        "email": data["email"],
        "personstatus": "student",
        "personid": student["id"],
    }

    user_back = UserRequest().create(user_data)
    user = User(username=data['login'], email=data['email'], first_name=data['name'],
                last_name=data['surname'], date_joined=datetime.datetime.today())
    user.set_password(data['password'])
    user.save()
    profile = user.profile
    profile.uid = user_back["id"]
    profile.save()


def is_email_valid(e_mail):
    """Проверка почты на валидность"""
    __email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return __email_re.match(e_mail)


def register_exception(_login, _password, _email):
    if len(User.objects.filter(username=_login)) > 0:
        return False, "Пользователь с данным логином уже существует!"
    if _login == "$_del":
        return False, "Логин не может быть '$_del'!"
    if not is_email_valid(_email):
        return False, "E-mail некорректен!"
    if len(User.objects.filter(email=_email)) > 0:
        return False, "Пользователь с указанным E-mail уже существует!"
    return True, None


def registration_page(request):
    """Регистрация"""
    context = get_context(request, "Регистрация")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context['form'] = form

        if not (form.is_valid()):
            context['res'] = "Неверно введены данные"
            return render(request, 'registration/registration.html', context)

        is_valid, error = register_exception(form.data['login'], form.data['password'], form.data['email'])

        if not is_valid:
            context['res'] = error
            print(error)
            return render(request, 'registration/registration.html', context)

        # Заполнение пользователя
        status = form.data['status']
        if status == "mentor":
            pass
        elif status == "student":
            register_student(form.data)
        else:
            error = "Добавлен несуществующий статус."
            context['res'] = error
            print(error)
            return render(request, 'registration/registration.html', context)

        mentor_data = {
            "id": "0",
            "name": "Ivan",
            "surname": "ivanov",
            "patronymic": "ivanivich",
            "birthdate": "12.02.2001",
            "interestsIDs": [],
            "likePersonsIDs": [],
            "dnlikePersonsIDs": []
        }

        return redirect('/login/')

    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'registration/registration.html', context)


#  Вход


def login_page(request):
    """Страница входа"""
    context = get_context(request, "Вход")
    if request.method == 'GET':
        context['form'] = LoginForm
        if auth.get_user(request).is_authenticated:
            return redirect('/')
        else:
            return render(request, 'registration/login.html', context=context)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        username = form.data["login"]
        password = form.data["password"]
        exists = usertool.check_user_existence(username, password)
        if exists:
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/')

        context['form'] = form
        context['error'] = "404"
        return render(request, 'registration/login.html', context=context)


def logout_view(request):
    auth.logout(request)
    return redirect('/')
