from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    # account_number =  models.CharField(max_length=10, unique=True)
  
    # USERNAME_FIELD = 'email'
    profile_photo = models.ImageField()
