from django.contrib.auth.models import User
from main.models import Mentor, Student, Theme, Interest, Profile


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


def get_user_by_mentor_id(mentor_id):
    try:
        profile = Profile.objects.get(person_id=mentor_id, status="mentor")
        user = profile.user
        return user, profile
    except Exception:
        return None, None


def get_user_by_student_id(student_id):
    try:
        return Profile.objects.get(person_id=student_id, status="student")
    except Exception:
        return None


def get_student_by_theme_id(theme_id):
    try:
        return Student.objects.get(theme_id=theme_id)
    except Exception:
        return None


def get_is_exist_theme(student_id):
    try:
        student = Student.objects.get(id=student_id)
        return student.theme_id
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
