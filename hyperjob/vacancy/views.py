from django.shortcuts import render, redirect
from vacancy.models import Vacancy
from django.views import View
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from django.forms import Form, CharField
 
 
# Create your views here.
class VacancyPage(View):
 
    def get(self, request, *args, **kwargs):
        return render(request, 'vacancy/vacancies.html', context={'vacancies': Vacancy.objects.all()})
 
 
class CreateVacancy(CreateView):
    class CreateForm(Form):
        description = CharField(label='Enter description', max_length=1024)
 
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return render(request, 'vacancy/new.html', context={'form': self.CreateForm})
        raise PermissionDenied
 
    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            form = self.CreateForm(request.POST)
            resumes = Vacancy.objects
            if form.is_valid():
                author, description = request.user, form.cleaned_data['description']
                new_vacancy = resumes.create(author=author, description=description)
                new_vacancy.save()
                return redirect('/home')
        raise PermissionDenied
