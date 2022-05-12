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


def is_email_valid(e_mail):
    """Проверка почты на валидность"""
    __email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return __email_re.match(e_mail)


def register_exception(_login, _password, _email):
    if len(User.objects.filter(username=_login)) > 0:
        return False, "Пользователь с данным логином уже существует!"
    if login == "$_del":
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

        isValid, error = register_exception(form.data['login'], form.data['password'], form.data['email'])

        if not isValid:
            context['res'] = error
            print(error)
            return render(request, 'registration/registration.html', context)

        # Заполнение пользователя
        user = User(username=form.data['login'], email=form.data['email'], first_name=form.data['name'],
                    last_name=form.data['surname'], date_joined=datetime.datetime.today())
        user.set_password(form.data['password'])
        user.save()
        # Заполнение профиля
        profile = user.profile
        profile.surname = form.data['surname']
        profile.name = form.data['name']
        # Проверка обязательных/необязательных полей
        if form.data['fathername'] != "":
            profile.fathername = form.data['fathername']
        if form.data['birth_year'].isdigit() and form.data['birth_month'].isdigit() and form.data[
            "birth_day"].isdigit():
            date = datetime.date(int(form.data['birth_year']),
                                 int(form.data['birth_month']),
                                 int(form.data['birth_day']))
            profile.birth_date = date
        if form.data['location'] != "":
            profile.location = form.data['location']
        if form.data['education_place'] != "":
            profile.education_place = form.data['education_place']
        profile.save()

        context['res'] = "Регистрация успешно завершена!"
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
