from django.shortcuts import render

# Create your views here.
# authentication/views.py

from . import forms
from django.contrib.auth import login, authenticate  # add to imports



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
            else:
     
                message = 'Login failed!'
            return render(request, 'login.html', context={'form': form,'message': message})

    elif request.method=='GET':
        return render(request,'login.html',context={'form': form,'message': ''})
