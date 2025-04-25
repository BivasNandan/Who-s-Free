from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import UserRegistrationForm
from django.contrib.auth import logout

# Create your views here.
def home(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, template_name='users/home.html', context=context)


def register(response):
    if response.method == 'POST':
        form = UserRegistrationForm(response.POST)

        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserRegistrationForm()
    
    return render(response, 'users/register.html', {'form': form})
