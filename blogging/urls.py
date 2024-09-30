from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("categoria/<categoria>/", views.blog_category, name="blog_categoria"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('eliminarComentario/<int:id>/', views.eliminar_comentario, name='eliminar_comentario'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)