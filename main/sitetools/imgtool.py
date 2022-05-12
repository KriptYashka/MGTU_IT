from django.templatetags.static import static
import random

def get_random_image_url():
    return static('img/article/{}.jpg'.format(random.randint(1, 10)))

def format_post_text(post_text):
    """Форматирование строки до лимита, переноса строки. Не обрывает слова."""
    limit = 80
    last_space = post_text[:limit].rfind(" ")
    if post_text.find("\n") >= limit:
        return post_text[:last_space]
    else:
        return post_text[:post_text.find("\n")]

def is_http_img(url):
    if str(url).find("http") == -1:
        return False
    return True

def check_media(arr):
    for item in arr:
        if not(is_http_img(item.img_url)) and (str(item.img_url) != ""):
            item.img_url = "/media/" + str(item.img_url)
    return arr