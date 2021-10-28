from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path

from accounts import views

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.profile_edit, name='profile_edit'),
]

