from django.contrib.auth.models import User

def check_user_existence(username, password):
    user = User.objects.filter(username=username)
    if len(user) != 1:
        return False
    user = user[0]
    return user.check_password(password)

def get_current_user(username):
    return User.objects.get(username=username)