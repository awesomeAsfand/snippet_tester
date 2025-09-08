from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard:dashboard')
                else:
                    form.add_error('username', 'Disabled account')

            else:
                form.add_error('password', "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Please correct the errors below.")
            # return render(request, "registration/login.html", {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})
