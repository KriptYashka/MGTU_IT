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
        response = requests.get(self.total_url, headers=self.headers)
        result = response.json()
        if response.status_code == 200:
            return result["value"]
        return None

    def get_by_id(self, obj_id: str):
        self.total_url += f"/{obj_id}"
        response = requests.get(self.total_url, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return result["value"]
        return None

    def create(self, obj_data: dict):
        response = requests.post(self.total_url, json=obj_data, headers=self.headers)
        result = response.json()
        print(response.status_code)
        if response.status_code == 200:
            return result["value"]
        return None

    def edit(self, obj_data: dict):
        response = requests.put(self.total_url, json=obj_data, headers=self.headers)
        return response.status_code

    def delete(self, obj_id: str):
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
    def __init__(self, type_req):
        self.id = None
        self.TypeRequest = type_req
        self.data = {"id": self.id}

    def load(self, uid):
        obj = self.TypeRequest().get_by_id(uid)
        if obj is not None:
            self.load_data_dict(obj)

    def load_data_dict(self, data_dict):
        for key in self.data:
            if key in data_dict.keys():
                self.data[key] = data_dict[key]

    def create(self, data_dict=None):
        if data_dict:
            self.load_data_dict(data_dict)
        obj = self.TypeRequest().create(self.data)
        if not obj:
            return Exception("Неверный запрос")
        # Обновление объекта
        self.load_data_dict(obj)

    def edit(self, data_dict=None):
        if data_dict:
            self.load_data_dict(data_dict)
        obj = self.TypeRequest().edit(self.data)
        if not obj:
            return Exception("Неверный запрос")
        # Обновление объекта
        self.load_data_dict(obj)

    def delete(self):
        cod = 400
        if self.id is not None or self.id is not id_none:
            cod = self.TypeRequest().delete(self.id)
        if cod != 200:
            return Exception("Неверный запрос")
        del self


class ModelRequestUser(ModelRequestBase):
    def __init__(self):
        super(ModelRequestUser, self).__init__(UserRequest)
        self.login = None
        self.password = None
        self.email = None
        self.person_status = None
        self.person_id = None
        self.photo = None

        self.data = {
            "id": self.id,
            "login": self.login,
            "password": self.password,
            "email": self.email,
            "personStatus": self.person_status,
            "personID": self.person_id,
            "photo": self.photo,
        }

        self.req_fields = {
            "create": ["login", "password"]  # TODO: требуется узнать у Сарибека
        }

    # def load(self, uid):
    #     user = UserRequest().get_by_id(uid)
    #     if user is not None:
    #         self.load_data_dict(user)
    #
    # def load_data_dict(self, data_dict):
    #     for key in self.data:
    #         if key in data_dict.keys():
    #             self.data[key] = data_dict[key]
    #
    # def create(self, data_dict=None, model_class=UserRequest):
    #     if data_dict:
    #         self.load_data_dict(data_dict)
    #     requirement = ["login", "password"]
    #     for key in requirement:
    #         if self.data[key] is None:
    #             return Exception("Не введен логин или пароль")
    #     user = UserRequest().create(self.data)
    #     if not user:
    #         return Exception("Неверный запрос")
    #
    #
    # def edit(self, data_dict=None):
    #     pass


class ModelRequestStudent:
    def __init__(self):
        self.id = None
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


class ModelRequestMentor:
    def __init__(self):
        self.id = None
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


class ModelRequestEvent:
    def __init__(self):
        self.id = None
        self.name_student = None
        self.surname_student = None
        self.patronymic_student = None
        self.birthdate_student = None
        self.group_student = None
        self.name_mentor = None
        self.surname_mentor = None
        self.patronymic_mentor = None
        self.birthdate_mentor = None
        self.category_id = None
        self.category_name = None
        self.theme_name = None


class ModelRequestTheme:
    def __init__(self):
        self.id = None
        self.theme_name = None


class ModelRequestCategory:
    def __init__(self):
        self.id = None
        self.category_name = None


if __name__ == '__main__':
    user = ModelRequestUser()
    data = {
        "login": "TestReq",
        "password": "123",
        "email": "email@lk.ru",
        "personStatus": "student",
        "personID": id_none,
    }
    user.create(data)
