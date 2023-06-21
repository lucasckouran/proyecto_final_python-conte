from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Adopcion(models.Model):
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    
    nombre = models.CharField(max_length=40)
    sexo = models.CharField(max_length=40, choices=SEXO_CHOICES)

    def __str__(self):
	    return f"Nombre: {self.nombre} - Sexo: {self.sexo}"

class Adoptante(models.Model):
	nombre = models.CharField(max_length=40)
	apellido = models.CharField(max_length=20)
	email = models.EmailField(max_length=40)
	def __str__(self):
		return f"Nombre: {self.nombre} - Apellido: {self.apellido} - email: {self.email}"

class Insumo(models.Model):
	producto = models.CharField(max_length=40)
	cantidad = models.IntegerField()
	tipo_producto_choices = [
        ('comida', 'Comida'),
        ('medicamento', 'Medicamento'),
    ]

	def __str__(self):
	    return f"Producto: {self.producto} - Cantidad: {self.cantidad}"


class Avatar(models.Model):
	#vinculo con el usuario
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	#subcarpeta avatares de media
	imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

	def __str__(self):
		return f"Avatar de {self.user.username}"