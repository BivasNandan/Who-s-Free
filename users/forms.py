from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import *

class Choose_User_Type(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = 'user_type',

class UserSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ]
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email = email):
            raise forms.ValidationError('An user with this email already exists!')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username = username):
            raise forms.ValidationError('A user with this username already exists!')
        return username
    
class BusinessSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email = email):
            raise forms.ValidationError('An user with this email already exists!')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'business'  # Set user type explicitly
        if commit:
            user.save()
        return user
    
class IndividualAdditionalInfo(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True)
    class Meta:
        model = CustomUser
        fields = [
            'profile_picture',
            'phone_number',
            'birth_date',
            'bio',
            'interests',
            'gender',
        ]

class BusinessAdditionalInfo(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'profile_picture',
            'phone_number',
            'company_name',
            'bio',
            'business_address',
            'website',
            'sector',
        ]