from main.sitetools.texttool import get_context
from main.sitetools import texttool, imgtool, usertool
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import dateformat


def news_page(request):
    """ Страница всех новостей """
    row_news_per_page = 4
    context = get_context(request, "Новости")
    template_path = 'pages/news.html'
    news = News.objects.all()
    pages = len(news) // (row_news_per_page * 4)
    if len(news) % (row_news_per_page * 4) != 0:
        pages += 1
    try:
        current_page = request.GET['page']
    except:
        current_page = "1"

    if current_page is None or not (current_page.isdigit()):
        current_page = 1
    current_page = int(current_page)
    context["count_pages"] = pages
    min_news_index = (current_page - 1) * row_news_per_page * 4
    max_news_index = min(current_page * row_news_per_page * 4, len(news))

    context['news'] = imgtool.check_media(news[min_news_index:max_news_index])
    context['page_nums'] = ["0" + str(item + 1) for item in range(0, pages)]

    return render(request, template_path, context)


def article_page(request, article_id):
    """ Страница новости. Подгружается контент с БД. """
    context = get_context(request, "Новость")
    template_path = 'pages/news_content.html'
    context['id'] = article_id
    article = News.objects.filter(id=article_id)[0]
    context['title'] = article.title
    context['pagename'] = article.title
    context['description'] = texttool.description_to_HTML(article.description)
    context['datetime'] = article.post_datetime.strftime("%d %b, %Y")
    if imgtool.is_http_img(str(article.img_url)):
        context['img_url'] = article.img_url
    else:
        context['img_url'] = "/media/" + str(article.img_url)
    if article.img_url == "" or article.img_url is None:
        context['img_url'] = imgtool.get_random_image_url()
    return render(request, template_path, context)

def announcement_page(request, page_id):
    """ Страница анонсов """
    context = get_context(request, "Анонс")
    announcement = Announcement.objects.filter(id=page_id)[0]
    context['item'] = announcement
    context['title'] = announcement.title
    template_path = 'pages/announcement.html'
    return render(request, template_path, context)

def projects_page(request):
    """Страница всех проектов"""
    context = get_context(request, "Проекты")
    template_path = 'pages/projects.html'
    return render(request, template_path, context)

def project_page(request, project_id):
    """Страница проекта"""
    context = get_context(request, "Проект")
    template_path = 'pages/project.html'
    context['id'] = project_id
    project = Projects.objects.filter(id=project_id)[0]
    context['title'] = project.title
    context['pagename'] = project.title
    context['description'] = texttool.description_to_HTML(project.description)
    context['datetime'] = project.post_datetime.strftime("%d %b, %Y")
    if imgtool.is_http_img(str(project.img_url)):
        context['img_url'] = project.img_url
    else:
        context['img_url'] = "/media/" + str(project.img_url)
    if project.img_url == "" or project.img_url is None:
        context['img_url'] = imgtool.get_random_image_url()
    return render(request, template_path, context)