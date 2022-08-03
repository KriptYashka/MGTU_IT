from django.contrib.auth.models import User
from main.models import Profile
from main.sitetools.backrequest import UserRequest


def check_user_existence(username, password):
    user = User.objects.filter(username=username)
    if len(user) != 1:
        return False
    user = user[0]
    return user.check_password(password)


def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except Exception:
        return None
