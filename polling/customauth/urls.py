from django.urls import path

from . import views


app_name = 'customauth'

urlpatterns =  [ 
    path('', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('home/',views.home, name='home'),
    path('signup/',views.signup_page, name='signup'),
 ]