from django.http import HttpResponseRedirect
from django.shortcuts import render
from blogging.models import Post, Comentario
from blogging.forms import CommentForm
from django.shortcuts import get_object_or_404

def blog_index(request):
    posts = Post.objects.all().order_by("-hora_creacion")
    context = {
        "posts": posts,
    }
    return render(request, 'index.html', context)

def acerca_de(request):
    posts = Post.objects.all().order_by("-hora_creacion")
    context = {
        "posts": posts,
    }
    return render(request, 'acerca_de.html', context)

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
                autor=form.cleaned_data["autor"],
                cuerpo=form.cleaned_data["body"],
                post=post,
            )
            comentarios.save()
            return HttpResponseRedirect(request.path_info)
    comments = Comentario.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, 'detail.html', context)
