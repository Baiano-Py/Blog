from django import forms
from blog.models import Profile, Post
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'description', 'photo',]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'excerpt', 'content', 'cover', 'category', 'tags', 'cover_in_post_content', 'is_published']