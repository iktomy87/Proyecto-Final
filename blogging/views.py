from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from blogging.models import Post, Comentario
from blogging.forms import CommentForm
from django.contrib.auth import login
from .forms import RegistroUsuarioForm


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
    context = {
        "categoria": categoria,
        "posts": posts,
    }
    return render(request, 'categoria.html', context)


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
    return render(request, 'registration/registro.html', {'form': form})