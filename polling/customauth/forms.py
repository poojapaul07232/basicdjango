# authentication/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    password = forms.PasswordInput()
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email','password1','password2')
        