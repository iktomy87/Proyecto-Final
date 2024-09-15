from django.contrib import admin
from blogging.models import Categoria, Comentario, Post

# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

class ComentarioAdmin(admin.ModelAdmin):
    pass

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comentario, ComentarioAdmin)
