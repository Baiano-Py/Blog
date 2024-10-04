from django.contrib import admin
from django.urls import path
from blog.views.blog_views import *
from blog.views.user_views import *


app_name = 'blog'

urlpatterns = [
    path('',  login, name='login'),
    path('register/',  register, name='register'),
    path('visitante/',  visitante, name='visitante'),
    path('logout/',  logout, name='logout'),


    #parte do home blog
    path('home/',  home, name='home'),
    path('post/<slug:slug>/', post, name='post'),

    path('category/<slug:slug>/', category, name='category'),
    path('tags/<slug:slug>/', tags, name='tags'),
    path('search/', search, name='search'),
    path('create/', create_post, name='create_post'),
    path('edit/<int:post_id>', edit_post, name='edit_post'),


    path('profile/<int:profile_id>/', profile, name='profile'),
    path('profile/edit/<int:profile_id>/', edit_profile, name='edit_profile'),
    path('profile/post/<int:profile_id>/', my_post, name='my_post'),
    path('profile/<int:profile_id>/follow/', follow_user, name='follow_user'),
    path('profile/<int:profile_id>/unfollow/', unfollow_user, name='un_follow_user'),
]