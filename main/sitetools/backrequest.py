import requests
import json

url = 'http://localhost:5000/'

id_none = "00000000-0000-0000-0000-000000000000"


class BackRequest:
    def __init__(self, postfix: str):
        self.postfix = postfix
        self.total_url = url + self.postfix
        self.headers = {
            'Content-Type': 'application/json',
            'Host': 'localhost',
            'User-Agent': 'PostmanRuntime/7.29.0',
        }

    def get_all(self):
        """
        Возвращает все объекты таблицы

        :return: Все объекты таблицы
        """
        response = requests.get(self.total_url, headers=self.headers)
        result = response.json()
        if response.status_code == 200:
            return result["value"]
        return None

    def get_by_id(self, obj_id: str):
        """
        Возвращает объект по id

        :return: Объект в таблице
        """
        self.total_url += f"/{obj_id}"
        response = requests.get(self.total_url, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return result["value"]
        return None

    def create(self, obj_data: dict):
        """
        Создает объект с данными словаря

        :return: Статус запроса
        """
        response = requests.post(self.total_url, json=obj_data, headers=self.headers)
        result = response.json()
        print(response.status_code)
        if response.status_code == 200:
            return result["value"]
        return None

    def edit(self, obj_data: dict):
        """
        Изменяет объект по данным словаря

        :return: Статус запроса
        """
        response = requests.put(self.total_url, json=obj_data, headers=self.headers)
        return response.status_code

    def delete(self, obj_id: str):
        """
        Удаляет объект по id

        :return: Статус запроса
        """
        self.total_url += f"/{obj_id}"
        response = requests.delete(self.total_url, headers=self.headers)
        return response.status_code


class StudentRequest(BackRequest):
    def __init__(self):
        super().__init__("student")


class MentorRequest(BackRequest):
    def __init__(self):
        super().__init__("mentor")


class UserRequest(BackRequest):
    def __init__(self):
        super().__init__("user")


class EventRequest(BackRequest):
    def __init__(self):
        super().__init__("event")


class ThemeRequest(BackRequest):
    def __init__(self):
        super().__init__("theme")


class CategoryRequest(BackRequest):
    def __init__(self):
        super().__init__("category")


def get_user_by_person(person_id):
    users = UserRequest().get_all()
    for user in users:
        if user["personID"] == person_id:
            return user
    return None


class ModelRequestBase:
    """
    Абстактный (в Питоне на уровне соглашений) класс моделей объектов БД
    """

    def __init__(self, obj_id, type_req):
        self.id = obj_id
        self.TypeRequest = type_req
        self.convert_data = {}

    def load(self, obj_id):
        """
        Находит объект в БД по id
        """
        obj = self.TypeRequest().get_by_id(obj_id)
        if obj is not None:
            self.load_data_dict(obj)

    def load_data_dict(self, data_dict):
        """
        Загружает объект по набору данных словаря
        """
        for db_name, front_name in self.convert_data.items():
            if db_name in data_dict.keys():
                self.__setattr__(front_name, data_dict[db_name])

    def get_db_data(self):
        """
        Возвращает словарь объекта со всеми полями, ключи которые используются в БД

        :return: Словарь объекта
        """
        db_data = dict()
        for db_name, front_name in self.convert_data.items():
            db_data[db_name] = self.__getattribute__(front_name)
        return db_data

    def create(self, data_dict=None):
        """
        Сохранение объекта в БД
        """
        if data_dict:
            self.load_data_dict(data_dict)
        obj = self.TypeRequest().create(self.get_db_data())
        if not obj:
            return Exception("Неверный запрос")
        # Обновление объекта
        self.load_data_dict(obj)

    def edit(self, data_dict=None):
        """
        Изменение и сохранение объекта в БД

        :param data_dict: Словарь данных, которые требуется изменить
        """
        if data_dict:
            self.load_data_dict(data_dict)
        cod = self.TypeRequest().edit(self.get_db_data())
        if cod != 200:
            return Exception("Неверный запрос")

    def delete(self, uid=None):
        """
        Удаление объекта из БД
        """
        cod = 400
        if uid is not None:
            self.id = uid
        if self.id is not None or self.id is not id_none:
            cod = self.TypeRequest().delete(self.id)
        if cod != 200:
            return Exception("Неверный запрос")
        del self

    def normalize_convert_data(self):
        """
        Преобразует словарь в новый без ключевых слов "self" и значений после знака "="
        """
        for key in self.convert_data.keys():
            index_equal = self.convert_data[key].rfind("=")  # Ищем последний знак "="
            self.convert_data[key] = self.convert_data[key][5:index_equal]

    def __bool__(self):
        if self.id is None or self.id is id_none:
            return False
        return True

    def __eq__(self, other):
        return bool(self) is other


class ModelRequestUser(ModelRequestBase):
    def __init__(self, uid=None):
        super(ModelRequestUser, self).__init__(uid, UserRequest)
        self.login = None
        self.password = None
        self.email = None
        self.person_status = None
        self.person_id = None
        self.photo = None

        #  Использование названия переменных по стандарту PEP8
        self.convert_data = {
            "id": f'{self.id=}',
            "login": f'{self.login=}',
            "password": f'{self.password=}',
            "email": f'{self.email=}',
            "personStatus": f'{self.person_status=}',
            "personID": f'{self.person_id=}',
            "photo": f'{self.photo=}',
        }
        self.normalize_convert_data()

        # self.req_fields = {
        #     "create": ["login", "password"]  # TODO: требуется узнать у бэкэндера
        # }

        if self.id is not None:
            self.load(uid)


class ModelRequestStudent(ModelRequestBase):
    def __init__(self, uid=None):
        super(ModelRequestStudent, self).__init__(uid, StudentRequest)
        self.name = None
        self.surname = None
        self.patronymic = None
        self.birthdate = None
        self.description = None
        self.status_pay = None
        self.group = None
        self.theme_id = None
        self.mentor_id = None
        self.interests_ids = None

        self.fullname = None

        self.convert_data = {
            "id": f'{self.id=}',
            "name": f'{self.name=}',
            "surname": f'{self.surname=}',
            "patronymic": f'{self.patronymic=}',
            "birthDate": f'{self.birthdate=}',
            "description": f'{self.description=}',
            "statusPay": f'{self.status_pay=}',
            "group": f'{self.group=}',
            "themeID": f'{self.theme_id=}',
            "mentorID": f'{self.mentor_id=}',
            "interestsIDs": f'{self.interests_ids=}',
        }
        self.normalize_convert_data()

        if self.id is not None:
            self.load(uid)
            self.fullname = f"{self.surname} {self.name} {self.patronymic}"


class ModelRequestMentor(ModelRequestBase):
    def __init__(self, uid=None):
        super(ModelRequestMentor, self).__init__(uid, MentorRequest)
        self.name = None
        self.surname = None
        self.patronymic = None
        self.birthdate = None
        self.description = None
        self.paid_students_left = None
        self.free_students_left = None
        self.all_students_left = None
        self.interests_ids = None
        self.like_persons_ids = None
        self.dislike_persons_ids = None

        self.fullname = None

        self.convert_data = {
            "id": f'{self.id=}',
            "name": f'{self.name=}',
            "surname": f'{self.surname=}',
            "patronymic": f'{self.patronymic=}',
            "birthDate": f'{self.birthdate=}',
            "description": f'{self.description=}',

            "paidStudentsLeft": f'{self.paid_students_left=}',
            "freeStudentsLeft": f'{self.free_students_left=}',
            "allStudentsLeft": f'{self.all_students_left=}',
            "interestsIDs": f'{self.interests_ids=}',
            "likePersonsIDs": f'{self.like_persons_ids=}',
            "DNLikePersonsIDs": f'{self.dislike_persons_ids=}',
        }
        self.normalize_convert_data()

        if self.id is not None:
            self.load(uid)
            self.fullname = f"{self.surname} {self.name} {self.patronymic}"

    def is_has_slot(self):
        if self.paid_students_left and self.free_students_left and self.all_students_left:
            return self.paid_students_left > 0 or self.free_students_left > 0 or self.all_students_left


class ModelRequestEvent(ModelRequestBase):
    class Student:
        def __init__(self):
            self.name = None
            self.surname = None
            self.patronymic = None
            self.birthdate = None
            self.group = None

            self.fullname = None

    class Mentor:
        def __init__(self):
            self.name = None
            self.surname = None
            self.patronymic = None
            self.birthdate = None

            self.fullname = None

    class Category:
        def __init__(self):
            self.id = None
            self.name = None

    class Theme:
        def __init__(self):
            self.name = None

    def __init__(self, event_id=None):
        super(ModelRequestEvent, self).__init__(event_id, EventRequest)
        self.student = self.Student()
        self.mentor = self.Mentor()
        self.category = self.Category()
        self.theme = self.Theme()

        self.convert_data = {
            "id": f'{self.id=}',

            "nameS": f'{self.student.name=}',
            "surnameS": f'{self.student.surname=}',
            "patronymicS": f'{self.student.patronymic=}',
            "birthDateS": f'{self.student.birthdate=}',
            "groupS": f'{self.student.group=}',

            "nameM": f'{self.mentor.name=}',
            "surnameM": f'{self.mentor.surname=}',
            "patronymicM": f'{self.mentor.patronymic=}',
            "birthDateM": f'{self.mentor.birthdate=}',

            "categoryNameID": f'{self.category.id=}',  # TODO: Потребовать от бэкэндера нормально назвать поле!
            "categoryName": f'{self.category.name=}',

            "themeName": f'{self.theme.name=}',
        }
        self.normalize_convert_data()

        if self.id is not None:
            self.load(event_id)


class ModelRequestTheme(ModelRequestBase):
    def __init__(self, theme_id=None):
        super(ModelRequestTheme, self).__init__(theme_id, ThemeRequest)
        self.name = None

        self.convert_data = {
            "id": f'{self.id=}',
            "themeName": f'{self.name=}',
        }
        self.normalize_convert_data()

        if self.id is not None:
            self.load(theme_id)


class ModelRequestCategory(ModelRequestBase):
    def __init__(self, category_id=None):
        super(ModelRequestCategory, self).__init__(category_id, CategoryRequest)
        self.name = None

        self.convert_data = {
            "id": f'{self.id=}',
            "categoryName": f'{self.name=}',
        }
        self.normalize_convert_data()

        if self.id is not None:
            self.load(category_id)


#  TODO: Сделать класс интересов


if __name__ == '__main__':
    user = ModelRequestUser()
    data = {
        "login": "TestReq",
        "password": "123",
        "email": "email@lk.ru",
        "personStatus": "student",
        "personID": id_none,
    }
    print(user.load("100422c2-4fb9-4817-adf8-d35cdd429a2e"))
    user.create(data)
