from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from main.sitetools import imgtool
from main.sitetools.texttool import get_context


@login_required
def main_activity_page(request):
    """ Страница всех мероприятий """
    context = get_context(request, "Мероприятия")
    context["activitys"] = Activity.objects.all()
    template_path = 'pages/main_activity.html'
    return render(request, template_path, context)

@login_required
def activity_page(request, activity_id):
    """ Страница мероприятия """
    context = get_context(request, "Мероприятие")

    activity = Activity.objects.filter(id=activity_id)[0]
    context["title"] = activity.title
    context["description"] = activity.description
    context["url"] = activity.url
    context["img_url"] = activity.img_url
    context["program"] = activity.program
    context["program_file"] = activity.program_file
    context["start_datetime"] = activity.start_datetime
    context["end_datetime"] = activity.end_datetime
    context["location"] = activity.location
    context["author"] = User.objects.filter(id=activity.author_id)[0]
    context["members"] = activity.members.all()
    context['img_url'] = "/media/" + str(activity.img_url)

    template_path = 'pages/activity.html'
    return render(request, template_path, context)

@login_required
def activity_create_page(request):
    """ Страница создания нового мероприятия """
    context = get_context(request, "Мероприятие")
    form = ActivityForm()
    context['form'] = form

    if request.method == 'POST':
        # Форма отправлена
        form = ActivityForm(request.POST)
        context['form'] = form
        if not(form.is_valid()):
            # Форма неверно заполнена
            context['res'] = "Неверно введены данные"
            return render(request, 'registration/registration.html', context)
        # Заполнение мероприятия

        activity = Activity(author_id=request.user.id,
                            title=form.data["title"],
                            url=form.data["url"],
                            description=form.data["description"],
                            program=form.data["program"],
                            program_file=form.data["program_file"],
                            location=form.data["location"],
                            start_datetime=form.data["start_datetime"],
                            end_datetime=form.data["end_datetime"],
                            )
        # img_url <=> img
        if imgtool.is_http_img(form.data["img_url"]):
            activity.img_url = form.data["img_url"]
        else:
            activity.img_url = form.data["img_file"]
        activity.save()
        context['res'] = "Мероприятие было создано."

    template_path = 'pages/activity_developing.html' # В разработке
    return render(request, template_path, context)

@login_required
def activity_edit_page(request, activity_id):
    """ Страница мероприятия, которая доступна для редактирования """
    context = get_context(request, "Мероприятие")
    # template_path = 'pages/activity.html'
    template_path = 'pages/activity_developing.html' # В разработке
    return render(request, template_path, context)