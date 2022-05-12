"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main.views import main_view, activity_view, registration_view, news_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', registration_view.login_page),
    path('logout/', registration_view.logout_view),
    path('registration/', registration_view.registration_page),

    path('', main_view.index_page),
    path('about/', main_view.about_page),
    path('profile/', main_view.profile_page),
    #
    # path('news/', news_view.news_page),
    # path('news/<int:article_id>', news_view.article_page),
    # path('announcement/<int:id>', news_view.announcement_page),
    #
    # path('activity/', activity_view.main_activity_page),
    # path('activity_create/', activity_view.activity_create_page),
    # path('activity_edit/<int:id>', activity_view.activity_edit_page),
    # path('activity/<int:activity_id>', activity_view.activity_page),
]
