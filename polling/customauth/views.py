from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
import logging, os
from django.core.files.storage import FileSystemStorage
from .facerecog import teachFace, findFace

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
        image = request.FILES['profile_photo']
        if not image:
            message = 'Login failed! No face found!'
            return render(request, 'login.html', context={'form': form,'message': message}, status=401)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                if user.profile_photo is None:
                    message = 'Login failed!'
                    return render(request, 'login.html', context={'form': form,'message': message}, status=401)
                fs = FileSystemStorage()
                filename='raw_'+user.get_username()+'.png'
                saved_raw = fs.save(filename, image)
                raw_file = os.path.join(settings.MEDIA_ROOT,saved_raw)
                model = os.path.join(settings.MEDIA_ROOT,user.profile_photo)
                status, msg = findFace(raw_file, model)
                if not status ==0:
                    message = 'Login failed! Face Not matched'
                    return render(request, 'login.html', context={'form': form,'message': message}, status=401)
                login(request, user)
                if os.path.exists(raw_file):
                    os.remove(raw_file)
                message = f'Hello {user.username}! You have been logged in'
                return redirect('polls/')
        message = 'Login failed!'
        return render(request, 'login.html', context={'form': form,'message': message}, status=401)

    elif request.method=='GET':
        return render(request,'login.html',context={'form': form,'message': ''})

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if not form.is_valid():
            logging.warning('Form Invalid')
            return render(request, 'signup.html', context={'form': form}, status=400)
        image = request.FILES['profile_photo']
        if not image:
            return render(request, 'signup.html', context={'form': form, 'message': 'picture not recieved'}, status=400)
        filename = image.name
        fs = FileSystemStorage()
        filename='raw_'+form.data['username']+'.png'
        saved_raw = fs.save(filename, image)
        raw_file = os.path.join(settings.MEDIA_ROOT,saved_raw)
        model = os.path.join(settings.MEDIA_ROOT,'model_'+form.data['username']+'.pkl')
        saved, message = teachFace(raw_file, form.data['username'], model)
        if saved != 0:
            return render(request, 'signup.html', context={'form': form, 'message': 'face register failed.'}, status=400)
        if os.path.exists(raw_file):
            os.remove(raw_file)
        user = form.save(commit=False)
        user.profile_photo = model
        user.save()
        # response = HttpResponseRedirect('')
        # response.status_code = 201
        return redirect('/')

    return render(request, 'signup.html', context={'form': form})
