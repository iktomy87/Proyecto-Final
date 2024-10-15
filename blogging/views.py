from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from blogging.models import Post, Comentario, Categoria
from blogging.forms import CommentForm
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
import requests
import os
from .forms import RegistroUsuarioForm
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Comentario
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


def grupo_requerido(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.groups.filter(name='Colaborador').exists())(view_func)

def no_autenticado(view_func):
    return user_passes_test(lambda u: not u.is_authenticated)(view_func)

def blog_index(request):
    posts = Post.objects.all().order_by("-hora_creacion")
    is_colab = request.user.groups.filter(name="Colaborador").exists()
    context = {
        "posts": posts,
        'is_colab': is_colab,
    }
    
    return render(request, 'index.html', context)

def blog_category(request, categoria):
    posts = Post.objects.filter(
        categorias__name__contains=categoria).order_by("-hora_creacion")
    is_colab = request.user.groups.filter(name="Colaborador").exists()
    context = {
        "categoria": categoria,
        "posts": posts,
        'is_colab': is_colab,
    }
    return render(request, 'categoria.html', context)


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    post.incrementar_visitas()
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
    }
    return render(request, 'detail.html', context)

def eliminar_comentario(request, id):
    comentario=Comentario.objects.get(id=id)
    comentario.delete()

    return redirect('blog_detail', pk=comentario.post.pk)

@csrf_exempt  # Solo si estás usando el método POST sin CSRF, no recomendado en producción
def actualizar_comentario(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nuevo_texto = data.get('nuevo_texto', '')

            # Busca el comentario por ID y actualiza el texto
            comentario = Comentario.objects.get(id=id)
            comentario.cuerpo = nuevo_texto
            comentario.save()

            return JsonResponse({'status': 'success', 'mensaje': 'Comentario actualizado'})
        except Comentario.DoesNotExist:
            return JsonResponse({'status': 'error', 'mensaje': 'Comentario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'}, status=405)

@no_autenticado
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

@grupo_requerido
def gestion_articulos(request):
    categorias = Categoria.objects.all()
    posts = Post.objects.all().order_by("-hora_creacion")
    is_colab = request.user.groups.filter(name="Colaborador").exists()
    context = {
        "categorias":categorias,
        "posts":posts,
        'is_colab': is_colab,
    }
    return render(request, 'gestion_articulos.html', context)

def crear_articulo(request):
    if request.method == 'POST':
        titulo = request.POST.get("txtTitulo")
        cuerpo = request.POST.get("txtCuerpo")
        imagen = request.FILES.get("imgFoto") 
        categorias_ids = request.POST.getlist("categorias[]")

        post = Post.objects.create(titulo=titulo, cuerpo=cuerpo, imagen=imagen)

        categorias = Categoria.objects.filter(id__in=categorias_ids)
        post.categorias.set(categorias)

        return redirect('/')

    return render(request, 'crear_articulo.html')

def eliminar_articulo(request, id):
    post=Post.objects.get(id=id)
    post.delete()

    return redirect('gestion_articulos')

@grupo_requerido
def edicion_articulo(request, id):
    categoriasunm = [] #categorias desmarcadas
    post = get_object_or_404(Post, id=id)
    categorias = Categoria.objects.all()

    for categoria in categorias:
        if categoria not in post.categorias.all():
            categoriasunm.append(categoria)

    context = {
        "categorias": categorias,
        "post": post,
        "categoriasunm": categoriasunm, 
    }

    return render(request, 'edicion_articulo.html', context)

def editar_articulo(request):
    if request.method == 'POST':
        id = int(request.POST["id"])
        titulo = request.POST.get("txtTitulo")
        cuerpo = request.POST.get("txtCuerpo")

        categorias_ids = request.POST.getlist("categorias[]")

        post=Post.objects.get(id=id)
        post.titulo=titulo
        post.cuerpo=cuerpo
        if 'imgFoto' in request.FILES:
            post.imagen = request.FILES['imgFoto']

        categorias = Categoria.objects.filter(id__in=categorias_ids)
        post.categorias.set(categorias)

        post.save()

        return redirect('/')

    return render(request, 'crear_articulo.html')

def blog_busqueda(request):
    is_colab = request.user.groups.filter(name="Colaborador").exists()
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            titulo__icontains=query
        ) | Post.objects.filter(
            cuerpo__icontains=query
        )
    else:
        posts = Post.objects.all() 

    context = {
        'is_colab': is_colab,
        'posts': posts,
        'query': query
    }
    return render(request, 'resultados.html', context)

def blog_contact(request):
    is_colab = request.user.groups.filter(name="Colaborador").exists()
    context = {
        'is_colab': is_colab,
    }
    return render(request, 'contacto.html',context)

def filtros(request):
    is_colab = request.user.groups.filter(name="Colaborador").exists()
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        posts = Post.objects.all().order_by('-titulo')
    elif order == 'asc':
        posts = Post.objects.all().order_by('titulo')
    elif order == 'reciente':
        posts = Post.objects.all().order_by('-hora_creacion')
    elif order == 'antiguo':
        posts = Post.objects.all().order_by('hora_creacion')
    
    context = {
        'is_colab': is_colab,
        'posts': posts
    }
    
    return render(request, 'filtros.html', context)

def get_weather(request, lat, lon):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)

def acerca_de(request):
    is_colab = request.user.groups.filter(name="Colaborador").exists()
    context = {
        'is_colab': is_colab,
    }
    return render(request, 'acerca_de.html',context)

def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('password')

        try:
            usuario = User.objects.get(username=username, email=email)
            usuario.set_password(new_password)  # Usar set_password para manejar el hash
            usuario.save()
            messages.success(request, "Contraseña cambiada correctamente")
            return redirect('login')  # Redirige a la página de éxito
        except User.DoesNotExist:
            messages.error(request, "Usuario o correo incorrectos")
    
    return render(request, "change_password.html") 