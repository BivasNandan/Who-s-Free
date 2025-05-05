from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import UserSignUpForm, BusinessSignUpForm, Choose_User_Type, IndividualAdditionalInfo, BusinessAdditionalInfo
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login

# Create your views here.
def home(request):
    return render(request, template_name='base.html')


def user_signup(request):#individually signing up
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'individual'  # Setting user type explicitly
            user.save()
            messages.success(request, 'Account Created Successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserSignUpForm()
    return render(request, 'users/user_signup.html', {'form': form})

def business_signup(request):
    if request.method == 'POST':
        form = BusinessSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'business'  # Explicitly set user type
            user.save()
            messages.success(request, 'Account Created Successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusinessSignUpForm()
    return render(request, 'users/business_signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not user.is_profile_complete:  # Check if the profile is incomplete
                if user.user_type == 'individual':
                    return redirect('individual_profile_setup')
                elif user.user_type == 'business':
                    return redirect('business_profile_setup')
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('account')  # Redirect to the account page after successful login
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)  # Log the user out
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to the login page after logout


def choose_user_type(request):
    if request.method == "POST":
        user_type = request.POST.get('user_type')
        if user_type in ['individual', 'business']:
            request.session['user_type'] = user_type  # Store user type in session
            return redirect('user_signup') if user_type == 'individual' else redirect('business_signup')
        else:
            messages.error(request, "Invalid user type selected.")
    return render(request, 'users/choose_user_type.html')


def individual_profile_setup(request):
    if request.method == 'POST':
        form = IndividualAdditionalInfo(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            request.user.is_profile_complete = True  # Mark profile as complete
            request.user.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('account')  # Redirect to the account page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = IndividualAdditionalInfo(instance=request.user)
    return render(request, 'users/individual_profile_setup.html', {'form': form})

def business_profile_setup(request):
    if request.method == 'POST':
        form = BusinessAdditionalInfo(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            request.user.is_profile_complete = True  # Mark profile as complete
            request.user.save()
            messages.success(request, 'Your business profile has been updated successfully!')
            return redirect('account')  # Redirect to the account page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusinessAdditionalInfo(instance=request.user)
    return render(request, 'users/business_profile_setup.html', {'form': form})

@login_required
def account_view(request):
    return render(request, 'users/account.html', {'user': request.user})




                        # FOR EVENTS

