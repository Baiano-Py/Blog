from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.forms import *
from blog.models import *
from django.db.models import Q
from django.utils.text import slugify



posts = list(range(1000))

@login_required
def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-pk')
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'title_site': 'Home'
        }
    )

@login_required
def post(request, slug):
    post = Post.objects.filter(is_published=True, slug=slug).first()
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
            'title_site': post.title
        }
    )

def category(request, slug):
    posts = Post.objects.filter(is_published=True, category__slug=slug).order_by('-pk')

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'title_site': slug,
        }
    )

def tags(request, slug):
    # Filtra os posts que têm a tag correspondente ao slug
    posts = Post.objects.filter(is_published=True, tags__slug=slug).order_by('-pk')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'title_site': slug,
        }
    )

def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = Post.objects.filter(
        Q(title__icontains=search_value) |
        Q(excerpt__icontains=search_value) |
        Q(content__icontains=search_value)
         ).order_by('-pk')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'search_value': search_value,
            'title_site': search_value,
        }
    )

def create_post(request):
    if not request.user.username == 'Visitante':
        categories = Category.objects.all()
        tags = Tag.objects.all()
        error_message = None  # Variável para armazenar a mensagem de erro
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.created_by = request.user

                # Gera o slug automaticamente se estiver vazio
                if not post.slug:
                    post.slug = slugify(post.title)

                # Verifica se o slug já existe
                if Post.objects.filter(slug=post.slug).exists():
                    error_message = "Este slug já está em uso. Tente outro."
                else:
                    post.save()
                    form.save_m2m()
                    return redirect('blog:home')
            else:
                print(form.errors)
        else:
            form = PostForm()

        return render(request, 'blog/pages/create_post.html', {
            'form': form,
            'categories': categories,
            'tags': tags,
            'error_message': error_message  # Passa a mensagem de erro
        })
    return redirect('blog:logout')

def edit_post(request, post_id):
    if not request.user.username == 'Visitante':
        categories = Category.objects.all()
        tags = Tag.objects.all()
        post = get_object_or_404(Post, id=post_id)  # Busca o post pelo ID

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)  # Preenche o formulário com os dados do post
            if form.is_valid():
                post = form.save(commit=False)  # Salva as alterações, mas não envia para o banco de dados ainda
                if not post.slug:  # Verifica se o slug não está definido
                    post.slug = slugify(post.title)  # Gera um slug baseado no título
                post.created_by = request.user
                post.save()  # Salva o post com o slug gerado
                return redirect('blog:home')  # Redireciona para a página inicial após salvar
        else:
            form = PostForm(instance=post)  # Cria o formulário com os dados do post para edição

        return render(request, 'blog/pages/edit_post.html', {'form': form, 'post': post, 'categories': categories, 'tags': tags})
    return redirect('blog:logout')