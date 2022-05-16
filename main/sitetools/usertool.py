from django.contrib.auth.models import User
from main.models import Mentor, Student, Theme, Interest


def check_user_existence(username, password):
    user = User.objects.filter(username=username)
    if len(user) != 1:
        return False
    user = user[0]
    return user.check_password(password)


def get_current_user(username):
    try:
        return User.objects.get(username=username)
    except Exception:
        return None

def get_mentor_by_id(mentor_id):
    try:
        return Mentor.objects.get(id=mentor_id)
    except Exception:
        return None


def get_student_by_id(student_id):
    try:
        return Student.objects.get(id=student_id)
    except Exception:
        return None


def get_theme_by_id(theme_id):
    try:
        return Theme.objects.get(id=theme_id)
    except Exception:
        return None


def get_interest_by_id(interest_id):
    try:
        return Interest.objects.get(id=interest_id)
    except Exception:
        return None
