from django.urls import path, re_path
from .views import VacancyPage, CreateVacancy
 
app_name = 'vacancy'
urlpatterns = [
    path('vacancies', VacancyPage.as_view()),
    re_path('vacancy/new/?', CreateVacancy.as_view()),
    ]

