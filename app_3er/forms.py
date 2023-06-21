from django import forms
from .models import Adopcion
# importaciones para usuarios ----------------------------------------------------------------------------------
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class AdopcionFormulario(forms.ModelForm):
    class Meta:
        model = Adopcion
        fields = ['nombre', 'sexo']
        widgets = {
            'sexo': forms.RadioSelect(choices=[('macho', 'Macho'), ('hembra', 'Hembra')]),
        }


class AdoptanteFormulario(forms.Form):
    nombre = forms.CharField(max_length=40)
    apellido = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=40)

class InsumoFormulario(forms.Form):
    tipo_producto_choices = [
        ('comida', 'Comida'),
        ('medicamento', 'Medicamento'),
    ]
	
    producto = forms.CharField(max_length=40)
    cantidad = forms.IntegerField()
    tipo_producto_choices = forms.ChoiceField(choices=tipo_producto_choices)


# vistas para usuarios
# ----------------------------------------------------------------------------------------------------------------------------------------------

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        # saca los mensajes de ayuda
        help_texts = {k: "" for k in fields}

        

class UserEditForm(UserCreationForm):
    # aca se definen las opciones que queremos modificar del usuario
    # ponemos las basicas

    email = forms.EmailField(label="Modificar Email")
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="repetir password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        # saca los mensajes de ayuda
        help_texts = {k: "" for k in fields}


class AvatarFormulario(forms.Form):
    imagen = forms.ImageField()