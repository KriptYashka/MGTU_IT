from django.contrib import admin
from django.urls import path

from main.views import main_view, registration_view, project_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', registration_view.login_page),
    path('logout/', registration_view.logout_view),
    path('registration/', registration_view.registration_page),

    path('', main_view.index_page),
    path('about/', main_view.about_page),
    path('profile/', main_view.profile_page),

    path('projects/', project_view.projects_page),
    path('project/<int:project_id>', project_view.project_page),
]
