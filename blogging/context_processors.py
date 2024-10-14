from .models import Post

def tendencias(request):
    posts_tendencias = Post.objects.order_by('-visitas')[:5]
    return {
        'posts_tendencias': posts_tendencias
    }