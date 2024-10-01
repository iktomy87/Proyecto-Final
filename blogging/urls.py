from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("categoria/<categoria>/", views.blog_category, name="blog_categoria"),
    path("contacto/", views.blog_contact, name="blog_contact"),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)