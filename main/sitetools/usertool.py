from django.contrib.auth.models import User
from main.models import Mentor, Student


def check_user_existence(username, password):
    user = User.objects.filter(username=username)
    if len(user) != 1:
        return False
    user = user[0]
    return user.check_password(password)


def get_current_user(username):
    return User.objects.get(username=username)


def get_mentor_by_id(mentor_id):
    return Mentor.objects.get(id=mentor_id)


def get_student_by_id(student_id):
    return Student.objects.get(id=student_id)
