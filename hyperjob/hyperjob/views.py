from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from resume.models import Resume
from django.core.exceptions import PermissionDenied
from vacancy.models import Vacancy
 
 
class MainPage(View):
    paths = ['vacancies', 'resumes', 'home', 'login', 'signup', 'logout']
 
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={'paths': self.paths})
 
 
class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if request.user.is_staff:
                vacancies = Vacancy.objects.filter(author=user)
                return render(request, 'home.html', context={'vacancies': vacancies,
                                                                      'user'     : user,
                                                                      'staff'    : user.is_staff})
            else:
                resumes = Resume.objects.filter(author=request.user)
                return render(request, 'home.html', context={'resumes': resumes,
                                                                      'user'   : user,
                                                                      'staff'  : user.is_staff})
        return redirect('/')
 
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('/resume/new')
        elif request.user.is_staff:
            return redirect('/vacancy/new')
        raise PermissionDenied
 
 
class SignupPage(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'
 
 
class LoginPage(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        form = AuthenticationForm
        return render(request, 'login.html', {'form': form})
 
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
        return render(request, 'login.html', {'form': form})
