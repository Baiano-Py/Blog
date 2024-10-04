from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import *





def register(request):
    errors = {}
    if request.method == 'GET':
        context = {'site_title': 'Blog -'}
        return render(request, 'blog/usuarios/register.html', context)
    
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    if User.objects.filter(username=username).exists():
        errors['register'] = 'esse nome de username já esta sendo utilizado'
        return render(request, 'blog/usuarios/error.html', {'errors': errors})
    if User.objects.filter(email=email).exists():
        errors['register'] = 'esse E-mail já foi registrado em outro usuario'
        return render(request, 'blog/usuarios/error.html', {'errors': errors})
    if len(password) < 8:
        errors['register'] = 'A senha precisa ter pelo menos 8 caracteres'
        return render(request, 'blog/usuarios/error.html', {'errors': errors})
    if password != confirm_password:
        errors['register'] = 'As duas senhas são diferentes'
        return render(request, 'blog/usuarios/error.html', {'errors': errors})



    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    return render(request, 'blog/usuarios/sucess.html')



def login(request):
    errors = {}
    if request.method == 'GET':
        context = {'site_title': 'Blog -'}
        return render(request, 'blog/usuarios/index.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username, password=password)

    if user:
        login_django(request, user)
        return render(request, 'blog/usuarios/sucess_login.html')
    else:
        errors['register'] = 'Nome de usuario ou login esta invalido'
        return render(request, 'blog/usuarios/error_login.html', {'errors': errors})
    
def visitante(request):
    errors = {}

    username = 'Visitante'
    password = '^tB2£9y"0(49\&'
    
    user = authenticate(username=username, password=password)

    if user:
        login_django(request, user) 
        return redirect('blog:home')

def logout(request):
    logout_django(request)
    return redirect('blog:login')

@login_required
def profile(request, profile_id):
    user = get_object_or_404(User, pk=profile_id)
    
    profile, created = Profile.objects.get_or_create(user=user)

    # Debug prints
    print(f"Requesting user: {request.user.username}")
    print(f"Profile user: {profile.user.username}")

    if request.user.username == 'Visitante':
        if request.user == user:
            return redirect('blog:logout')

    posts = Post.objects.filter(is_published=True, created_by=user).order_by('-pk')
    
    # Verifica se o usuário está seguindo
    is_following = Follow.objects.filter(user=request.user, following=user).exists()
    
    print(f"Is following: {is_following}")  # Aqui você pode ver o resultado

    first_post = posts.first()  
    post_count = posts.count() 

    return render(
        request,
        'blog/pages/profile.html',
        {
            'user': user,        
            'profile': profile,  
            'posts': first_post, 
            'post_count': post_count,
            'title_site': user,
            'is_following': is_following,
        }
    )

@login_required
def edit_profile(request, profile_id):
    if not request.user.username == 'Visitante':
        user = get_object_or_404(User, pk=profile_id)
        profile = get_object_or_404(Profile, user=user)

        if request.method == 'POST':
            profile.name = request.POST.get('username')
            profile.description = request.POST.get('description')
            
            # Verifica se há um arquivo de imagem e o salva
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            
            profile.save()  # Salva o perfil
            return redirect('blog:profile', profile_id=user.id)

        return render(request, 'blog/pages/edit_profile.html', {'user': user, 'profile': profile})
    return redirect('blog:logout')

def my_post(request, profile_id):
        posts = Post.objects.filter(is_published=True, created_by=profile_id).order_by('-pk')
        paginator = Paginator(posts, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'blog/pages/index.html',
            {
                'page_obj': page_obj,
                'title_site': 'My Post',
            }
        )

@login_required
def follow_user(request, profile_id):
    if request.user.username != 'Visitante':
        user_to_follow = get_object_or_404(User, id=profile_id)
        profile = get_object_or_404(Profile, user=user_to_follow)

        # Verifica se o usuário já está seguindo
        if not Follow.objects.filter(user=request.user, following=user_to_follow).exists():
            # Adiciona o novo Follow
            Follow.objects.create(user=request.user, following=user_to_follow)
            profile.followers_count += 1
            profile.save()
        
        return redirect('blog:profile', profile_id=profile_id)
    else:
        return redirect('blog:logout')

@login_required
def unfollow_user(request, profile_id):
    user_to_unfollow = get_object_or_404(User, id=profile_id)

    try:
        # Encontrar o objeto Follow correspondente
        follow = Follow.objects.get(user=request.user, following=user_to_unfollow)
        follow.delete()  # Remove o registro de seguir
        
        # Reduzir o contador de seguidores
        profile = get_object_or_404(Profile, user=user_to_unfollow)
        profile.followers_count -= 1
        profile.save()
        
    except Follow.DoesNotExist:
        pass  # O usuário já não está seguindo

    return redirect('blog:profile', profile_id=profile_id)