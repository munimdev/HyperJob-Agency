from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from .models import Resume
from django.core.exceptions import PermissionDenied
from django.forms import Form, CharField


# Create your views here.
class ResumePage(View):
    resumes = Resume.objects

    def get(self, request, *args, **kwargs):
        return render(request, 'resume/resumes.html', context={'resumes': self.resumes.all()})


class CreateForm(Form):
    description = CharField(label='Enter description', max_length=1024)


class CreateResume(CreateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return render(request, 'resume/new.html', context={'form': CreateForm})
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            form = CreateForm(request.POST)
            resumes = Resume.objects
            if form.is_valid():
                author, description = request.user, form.cleaned_data['description']
                new_resume = resumes.create(author=author, description=description)
                new_resume.save()
                return redirect('/home')
        raise PermissionDenied
