from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("categoria/<categoria>/", views.blog_category, name="blog_categoria"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('eliminarComentario/<int:id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('comentarios/actualizar/<int:id>/', views.actualizar_comentario, name='actualizar_comentario'),
    path('busqueda/', views.blog_busqueda, name='blog_busqueda'),
    path("acerca-de/", views.acerca_de, name="acerca_de"),
    path("contacto/", views.blog_contact, name="blog_contact"),
    path('filtros/', views.filtros, name='filtros'),
    path('get_weather/<str:lat>/<str:lon>/', views.get_weather, name='get_weather'),
    path('gestionArticulos/', views.gestion_articulos, name='gestion_articulos'),
    path('crearArticulo/', views.crear_articulo, name='crear_articulo'),
    path('eliminarArticulo/<int:id>', views.eliminar_articulo, name='eliminar_articulo'),
    path('edicionArticulo/<int:id>', views.edicion_articulo, name="edicion_articulo"),
    path('editarArticulo/', views.editar_articulo, name='editar_articulo'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html')),
    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)