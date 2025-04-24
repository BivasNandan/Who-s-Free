from django.shortcuts import render
from .models import CustomUser

# Create your views here.
def home(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, template_name='users/home.html', context=context)