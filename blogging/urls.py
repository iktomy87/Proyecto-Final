from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("categoria/<categoria>/", views.blog_category, name="blog_categoria"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('eliminarComentario/<int:id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('busqueda/', views.blog_busqueda, name='blog_busqueda'),
    path("acerca-de/", TemplateView.as_view(template_name="acerca_de.html"), name="acerca_de"),
    path("contacto/", views.blog_contact, name="blog_contact"),
    path('filtros/', views.filtros, name='filtros'),
    path('get_weather/<str:lat>/<str:lon>/', views.get_weather, name='get_weather'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)