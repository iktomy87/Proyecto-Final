from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Tu comentario"}
        )
    )

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']