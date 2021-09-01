from django.urls import path, re_path
from .views import ResumePage, CreateResume

app_name = 'resume'
urlpatterns = [
    path('resumes', ResumePage.as_view()),
    re_path('resume/new/?', CreateResume.as_view()),
    ]