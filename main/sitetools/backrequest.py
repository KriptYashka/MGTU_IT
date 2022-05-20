import requests
import json

url = 'http://localhost:5000/'

#  Students


def get_students():
    total_url = url + "student"
    response = requests.get(total_url)
    result = response.json()
    if response.status_code == 200:
        return result["value"]
    return None


def get_student_by_id(student_id: str):
    total_url = url + "student/" + student_id
    response = requests.get(total_url)
    if response.status_code == 200:
        result = response.json()
        return result["value"]
    return None


def create_student(student_data):
    total_url = url + "student/"
    response = requests.post(total_url, data=student_data)
    return response.status_code


def edit_student(student_data):
    total_url = url + "student/"
    response = requests.put(total_url, data=student_data)
    return response.status_code


def delete_student(student_id: str):
    total_url = url + "student/" + student_id
    response = requests.delete(total_url)
    return response.status_code


if __name__ == '__main__':
    res = get_student_by_id("90ecf692-f920-4779-8bee-44e155c6ef24")
    print(res)
