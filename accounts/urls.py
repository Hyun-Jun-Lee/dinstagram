from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('password_change/', views.Password_Change_View.as_view(), name='password_change'),
]

