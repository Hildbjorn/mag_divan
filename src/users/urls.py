from django.urls import path
from .views import *

urlpatterns = [
    path('', ProfileUpdateView.as_view(), name='profile'),
    path('signup/', SignUpView.as_view(), name='profile_signup'),
    path('login/', CustomLoginView.as_view(), name='profile_login'),
    path('logout/', CustomLogoutView.as_view(), name='profile_logout'),
    path('profile_activate/<uidb64>/<token>/',
         profile_activate, name='profile_activate'),
    path('delete/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('all_users/', AllUsersView.as_view(), name='all_users'),
    path('email_confirm_done/', email_confirm_done, name='email_confirm_done'),
]
