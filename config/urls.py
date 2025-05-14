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
    path('', u_views.home, name='home'),

    #for users
    path('user_signup/', u_views.user_signup, name='user_signup'),
    path('business_signup/', u_views.business_signup, name='business_signup'),
    path('login/', u_views.login_view, name = 'login'),
    path('logout/', u_views.logout_view, name = 'logout'),
    path('individual_profile_setup/', u_views.individual_profile_setup, name='individual_profile_setup'),
    path('business_profile_setup/', u_views.business_profile_setup, name='business_profile_setup'),
    path('choose_user_type/', u_views.choose_user_type, name='choose_user_type'),
    path('account/', u_views.account_view, name = 'account'),
    path('create/', u_views.create, name = 'create'),

    #handles friend aspect of things
    path('send_friend_request/<uuid:id>/', u_views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:id>/', u_views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:id>/', u_views.reject_friend_request, name='reject_friend_request'),
    path('friend_list/', u_views.friend_list, name='friend_list'),
    path('friend_requests/', u_views.friend_requests, name='friend_requests'),
    path('delete_friend/<uuid:user_id>/', u_views.delete_friend, name='delete_friend'),

    #for events
    path('events_list/', e_views.events_list, name='events_list'),
    path('create_event/', e_views.create_event, name='create_event'),
    path('update/<uuid:id>/', e_views.update_event, name='update_event'),
    path('delete/<uuid:id>/', e_views.delete_event, name='delete_event'),
    path('interested/<uuid:event_id>/', e_views.mark_interested, name='mark_interested'),
    path('my_created_events/', e_views.my_created_events, name='my_created_events'),
    path('my_interested_event/', e_views.my_interested_event, name='my_interested_event'),
    path('interested_users/<uuid:id>/', e_views.interested_users, name='interested_users'),

    #for chat
    path('<uuid:user_id>/', c_views.chat_room, name='chat_room'),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
