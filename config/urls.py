"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from users import views as u_views
from events import views as e_views
from chat import views as c_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', u_views.home),
    path('events/', e_views.home),
    path('chat/', c_views.home),
    path('register/', u_views.register, name='register'),
    path('', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
