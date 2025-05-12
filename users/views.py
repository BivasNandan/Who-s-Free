from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Friendship
from .forms import UserSignUpForm, BusinessSignUpForm, Choose_User_Type, IndividualAdditionalInfo, BusinessAdditionalInfo
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request, template_name='landing_page.html')


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

@login_required
def send_friend_request(request, id):
    to_user = get_object_or_404(CustomUser, id=id)
    if Friendship.objects.filter(from_user=request.user, to_user=to_user).exists():
        messages.error(request, "Friend request already sent.")
    else:
        Friendship.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, "Friend request sent.")
    return redirect('account')

@login_required
def accept_friend_request(request, id):
    friend_request = get_object_or_404(Friendship, id=id, to_user=request.user)
    friend_request.status = 'accepted'
    friend_request.save()
    messages.success(request, "Friend request accepted.")
    return redirect('account')

@login_required
def reject_friend_request(request, id):
    friend_request = get_object_or_404(Friendship, id=id, to_user=request.user)
    friend_request.status = 'rejected'
    friend_request.save()
    messages.success(request, "Friend request rejected.")
    return redirect('account')


@login_required
def friend_list(request):
    """View to display the user's friends."""
    friends = request.user.friends()
    return render(request, 'users/friend_list.html', {'friends': friends})

@login_required
def friend_requests(request):
    """View to display the user's received friend requests."""
    friend_requests = request.user.friend_requests()
    return render(request, 'users/friend_requests.html', {'friend_requests': friend_requests})

@login_required
def delete_friend(request, user_id):
    """Delete a friend relationship."""
    friend = get_object_or_404(CustomUser, id=user_id)
    # Check if the friendship exists
    friendship = Friendship.objects.filter(
        (Q(from_user=request.user, to_user=friend) | Q(from_user=friend, to_user=request.user)),
        status='accepted'
    ).first()

    if friendship:
        friendship.delete()
        messages.success(request, f"You have removed {friend.username} from your friends.")
    else:
        messages.error(request, "You are not friends with this user.")
    return redirect('friend_list')