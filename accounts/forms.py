from django.contrib.auth.forms import UserCreationForm

from .models import User
from django import forms

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','first_name','last_name']
    pass
