from django.shortcuts import render
from django.conf import settings


# Create your views here.
# authentication/views.py

from . import forms
from django.contrib.auth import login,authenticate ,logout # add to imports
from django.shortcuts import redirect, render


def logout_user(request):
    logout(request)
    return redirect('/')

def login_page(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                return redirect('polls/')
        message = 'Login failed!'
        return render(request, 'login.html', context={'form': form,'message': message})

    elif request.method=='GET':
        return render(request,'login.html',context={'form': form,'message': ''})

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('/account/profile')
    return render(request, 'signup.html', context={'form': form})
