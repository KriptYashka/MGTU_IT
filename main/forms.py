from django import forms
from django.contrib import admin


class CommonFields:
    """ Общий класс всех полей, заранее проверяет на наличие ошибок """

    @staticmethod
    def get_title_field(label="Название", is_required=True):
        attrs = {"class": "form-control"}
        return forms.CharField(label=label, min_length=1, max_length=32, required=is_required,
                               widget=forms.TextInput(attrs=attrs))

    @staticmethod
    def get_password_field(label="Пароль", is_required=True):
        attrs = {"class": "form-control"}
        return forms.CharField(label=label, min_length=1, max_length=32, required=is_required,
                               widget=forms.PasswordInput(attrs=attrs))

    @staticmethod
    def get_int_field(label="Число", is_required=True):
        attrs = {"class": "form-control"}
        return forms.IntegerField(label=label, required=is_required, widget=forms.NumberInput(attrs=attrs))

    @staticmethod
    def get_editor_field(label="Описание", is_required=True):
        attrs = {"class": "form-control"}
        return forms.CharField(label=label, min_length=1, max_length=300, required=is_required,
                               widget=forms.Textarea(attrs=attrs))


class LoginForm(forms.Form):
    """Форма для страницы логина"""
    attrs = {
        "class": "input100",
        "data-placeholder": "Логин или E-Mail",
    }
    login = forms.CharField(label="Логин", min_length=1, max_length=64, required=True,
                            widget=forms.TextInput(attrs=attrs))

    attrs = {
        "class": "input100",
        "data-placeholder": "Пароль"
    }
    password = forms.CharField(label="Пароль", min_length=1, max_length=64, required=True,
                               widget=forms.PasswordInput(attrs=attrs))


class RegistrationForm(forms.Form):
    """ Форма регистрации пользователя.
    Параметры полей: описание поля; обязательное поле """
    login = CommonFields.get_title_field("Никнейм")
    surname = CommonFields.get_title_field("Фамилия")
    name = CommonFields.get_title_field("Имя")
    fathername = CommonFields.get_title_field("Отчество")
    password = CommonFields.get_password_field("Пароль")
    password_repeat = CommonFields.get_password_field("Повторите пароль")
    birth_day = CommonFields.get_int_field("День")
    birth_month = CommonFields.get_int_field("Месяц")
    birth_year = CommonFields.get_int_field("Год")
    email = CommonFields.get_title_field("E-Mail")
    attrs = {
        "class": "input100",
        "data-placeholder": "Пароль"
    }
    status = forms.ChoiceField(label="Вид аккаунта", required=True,
                               choices=(("mentor", "Преподаватель"),
                                        ("student", "Студент"),
                                        ("admin", "Администратор")),
                               widget=forms.Select(attrs=attrs))
    group = CommonFields.get_title_field("Группа (если студент)", False)


class ProfileForm(forms.Form):
    login = CommonFields.get_title_field("Никнейм")
    surname = CommonFields.get_title_field("Фамилия")
    name = CommonFields.get_title_field("Имя")
    fathername = CommonFields.get_title_field("Отчество")
    email = CommonFields.get_title_field("E-Mail")
    about = CommonFields.get_title_field("О себе", False)


# class ActivityForm(forms.Form):
#     title = CommonFields.get_title_field("Название мероприятия")
#     img_url = forms.FileField(label="Обложка мероприятия. Изображение не больше 4 МБ.")
#     url = forms.URLField(label="Ссылка на мероприятия")
#     description = CommonFields.get_editor_field("Описание мероприятия")
#     program = CommonFields.get_editor_field("Программа мероприятия")
#     program_file = forms.FileField(label="Файл программы мероприятия")
#     location = forms.CharField(label="Место проведения")
#     start_datetime = forms.DateTimeField(label="Начало мероприятия")
#     end_datetime = forms.DateTimeField(label="Конец мероприятия")

class InterestForm(forms.Form):
    name = CommonFields.get_title_field("Название")


class ThemeForm(forms.Form):
    name = CommonFields.get_editor_field("Название темы")
    # interest = CommonFields.get_title_field("Категория")

# # Классы админской панели
# class AdminActivityForm(forms.ModelForm):
#     # title = forms.CharField()
#     # author = forms.CharField(required=False)
#     # img_url = forms.CharField(required=False)
#     # description = forms.CharField(widget=forms.Textarea)
#     # datetime_start = forms.DateTimeField()
#     # datetime_end = forms.DateTimeField()
#     # activity_url = forms.CharField(required=False)
#     # location = forms.CharField(required=False)
#     class Meta:
#         model = Activity
#         fields = '__all__'


# class AdminNewsForm(forms.ModelForm):
#     title = forms.CharField()
#     img_url = forms.FileField(required=False, help_text="Изображение новости. Не больше 4 МБ.")
#     description = forms.CharField(widget=forms.Textarea)
#
#     class Meta:
#         model = News
#         fields = '__all__'
#
#
# class AdminAnnouncementForm(forms.ModelForm):
#     title = forms.CharField()
#     img_url = forms.FileField(required=False)
#     description = forms.CharField(widget=forms.Textarea)
#     url = forms.CharField()
#
#     class Meta:
#         model = Announcement
#         fields = '__all__'
#
#
# class News_Admin(admin.ModelAdmin):
#     form = AdminNewsForm
#
#
# class Activity_Admin(admin.ModelAdmin):
#     form = AdminActivityForm
#
#
# class Announcement_Admin(admin.ModelAdmin):
#     form = AdminAnnouncementForm
