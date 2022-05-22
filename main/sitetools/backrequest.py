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


if __name__ == '__main__':
    data = {
        "id": "3b79529f-a457-4d52-888d-2bfadddbd5e9",
        "name": "EGOR",
        "surname": "Kuchuk",
    }
    res = StudentRequest().get_all()
    print(res)
