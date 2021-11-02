from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path,re_path, reverse_lazy
from django.contrib.auth import views as auth_views
from accounts import views


urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('password_change/', views.Password_Change_View.as_view(), name='password_change'),
    re_path(r'^(?P<username>[\w.@+-]+)/follow/$', views.user_follow, name='user_follow'),
    re_path(r'^(?P<username>[\w.@+-]+)/unfollow/$', views.user_unfollow, name='user_unfollow'),

]

