from typing import List

from main.sitetools.backrequest import EventRequest, StudentRequest, ThemeRequest, id_none, ModelRequestStudent, \
    MentorRequest, ModelRequestMentor


class Project:
    """
    Класс проекта, хранящий информацию о теме проекта (Theme) и о студенте (Student), который создал данную тему.
    """

    def __init__(self, project_id: str, title: str, student):
        self.id = project_id
        self.title = title
        self.student = student
        self.path = f"img/article/{get_rand_num(project_id)}.jpg"


def get_rand_num(uid: str):
    """
    Возвращает число в зависимости от id nользователя

    :param uid: ID пользователя
    :return: Сумма цифр в id пользователя
    """
    sum = 0
    for symbol in uid:
        if symbol.isnumeric():
            sum += int(symbol)
    return sum % 10 + 1


def create_event(student: dict, mentor: dict, theme_name: str):
    """
    Передает данные и создает новый объект в БД.

    :param student: Прикрепляющийся словарь студента
    :param mentor: Прикрепляющийся словарь ментора
    :param theme_name: Название темы проекта
    """
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


def get_all_projects():
    """
    Возвращает все проекты студентов.

    :return: Все проекты студентов
    """
    students = StudentRequest().get_all()
    projects = []
    for student in students:
        if student["themeID"] != id_none:
            theme = ThemeRequest().get_by_id(student["themeID"])
            project = Project(theme["id"], theme["themeName"], student)
            projects.append(project)
    return projects


def get_all_mentors() -> List[ModelRequestMentor]:
    """
    Возвращает всех менторов

    :return: Всех менторов
    """
    mentors = []
    mentors_dict = MentorRequest().get_all()
    for mentor_dict in mentors_dict:
        mentor = ModelRequestMentor(mentor_dict)
        mentors.append(mentor)
    return mentors


def get_student_by_theme_id(theme_id: str) -> ModelRequestStudent:
    """
    Возвращает студента, прикрепленного к теме

    :param theme_id: ID темы
    :return: Модель студента, прикрепленного к теме
    """
    students = StudentRequest().get_all()
    student_dict = None
    for student in students:
        if student["themeID"] == theme_id:
            student_dict = student
            break
    student = ModelRequestStudent()
    student.load_data_dict(student_dict)
    return student
