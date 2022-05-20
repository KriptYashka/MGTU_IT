import requests
import json

url = 'http://localhost:5000/'


class BackRequest:
    def __init__(self, postfix: str):
        self.postfix = postfix
        self.total_url = url + self.postfix

    def get_all(self):
        response = requests.get(self.total_url)
        result = response.json()
        if response.status_code == 200:
            return result["value"]
        return None

    def get_by_id(self, obj_id: str):
        self.total_url += f"/{obj_id}"
        response = requests.get(self.total_url)
        if response.status_code == 200:
            result = response.json()
            return result["value"]
        return None

    def create(self, data: dict):
        response = requests.post(self.total_url, data=data)
        return response.status_code

    def edit(self, data: dict):
        response = requests.put(self.total_url, data=data)
        return response.status_code

    def delete(self, obj_id: str):
        self.total_url += f"/{obj_id}"
        response = requests.put(self.total_url)
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
    res = StudentRequest().get_all()
    print(res)
