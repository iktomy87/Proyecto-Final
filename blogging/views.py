from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from blogging.models import Post, Comentario
from blogging.forms import CommentForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.http import JsonResponse
import requests
import os
from .forms import RegistroUsuarioForm


def blog_index(request):
    posts = Post.objects.all().order_by("-hora_creacion")
    is_colab = request.user.groups.filter(name="Colaborador").exists()
    posts_tendencias = Post.objects.order_by('-visitas')[:5]
    context = {
        "posts": posts,
        'is_colab': is_colab,
        "posts_tendencias": posts_tendencias,
    }
    
    return render(request, 'index.html', context)

def blog_category(request, categoria):
    posts = Post.objects.filter(
        categorias__name__contains=categoria).order_by("-hora_creacion")
    context = {
        "categoria": categoria,
        "posts": posts,
    }
    return render(request, 'categoria.html', context)


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.incrementar_visitas()
    posts_tendencias = Post.objects.order_by('-visitas')[:5]
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comentarios = Comentario(
                autor=request.user,
                cuerpo=form.cleaned_data["body"],
                post=post,
            )
            comentarios.save()
            return HttpResponseRedirect(request.path_info)
    comments = Comentario.objects.filter(post=post)
    is_colab = request.user.groups.filter(name="Colaborador").exists()
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
        'is_colab': is_colab,
        "posts_tendencias": posts_tendencias,
    }
    return render(request, 'detail.html', context)

def eliminar_comentario(request, id):
    comentario=Comentario.objects.get(id=id)
    comentario.delete()

    return redirect('blog_detail', pk=comentario.post.pk)

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guardamos el nuevo usuario
            login(request, user)  # Iniciamos sesión automáticamente
            return redirect('/')  # Redireccionamos a una página después de registrar
    else:
        form = RegistroUsuarioForm()
    return render(request, 'register.html', {'form': form})


def blog_busqueda(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            titulo__icontains=query
        ) | Post.objects.filter(
            cuerpo__icontains=query
        )
    else:
        posts = Post.objects.all() 
    return render(request, 'resultados.html', {'posts': posts, 'query': query})

def blog_contact(request):
    return render(request, 'contacto.html')

def filtros(request):
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        posts = Post.objects.all().order_by('-titulo')
    elif order == 'asc':
        posts = Post.objects.all().order_by('titulo')
    elif order == 'reciente':
        posts = Post.objects.all().order_by('-hora_creacion')
    elif order == 'antiguo':
        posts = Post.objects.all().order_by('hora_creacion')
    
    return render(request, 'filtros.html', {'posts': posts})

def get_weather(request, lat, lon):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)



