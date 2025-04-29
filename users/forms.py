from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserSignUpForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, label='What are you registering as?')
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
            'user_type',
        ]
    def clean_mail(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email = email):
            raise forms.ValidationError('A user with this email already exists')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username = username):
            raise forms.ValidationError('A user with this username already exists')
        return username
        
        

