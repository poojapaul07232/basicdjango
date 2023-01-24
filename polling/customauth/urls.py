from django.urls import path

from . import views


app_name = 'customauth'

urlpatterns =  [ 
    path('', views.login_page, name='login'),

 ]