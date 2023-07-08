from django.shortcuts import render
from django.contrib.auth.models import User 
from django_countries.fields import CountryField

class UserProfile(models.model):
    """ A user profile model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)

