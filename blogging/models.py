from django.db import models
from django.conf import settings

# Create your models here.

class Categoria(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name

class Post(models.Model):
    titulo = models.CharField(max_length=255)
    cuerpo = models.TextField()
    hora_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_cambio = models.DateTimeField(auto_now=True)
    categorias = models.ManyToManyField("Categoria", related_name="posts")
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)
    visitas = models.IntegerField(default=0)

    def incrementar_visitas(self):
        self.visitas += 1
        self.save()

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cuerpo = models.TextField()
    hora_creacion = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.autor} on '{self.post}'"