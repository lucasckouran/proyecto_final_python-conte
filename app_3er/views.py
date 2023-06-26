from django.shortcuts import render, redirect
from app_3er.forms import *
from app_3er.models import *
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
# importaciones para usuarios ----------------------------------------------------------------------------------
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User



def index(request):
	avatares = Avatar.objects.filter(user=request.user.id)
	url = avatares[0].imagen.url if avatares else ''  # Obtener la URL del avatar o una cadena vacía si no hay avatar
	return render(request, "app_3er/index.html", {"url": url})

def adopciones(request):
	if request.method == "POST":
		miFormulario = AdopcionFormulario(request.POST)
		print(miFormulario)

		if miFormulario.is_valid():
			informacion = miFormulario.cleaned_data
			adopcion = Adopcion(nombre = informacion["nombre"], sexo = informacion["sexo"])
			adopcion.save()
			return render(request,"app_3er/leergatos.html")
		
	else:
		miFormulario = AdopcionFormulario()

	return render(request, "app_3er/adopciones.html",{"miFormulario":miFormulario})
	# return render(request, "app_3er/adopciones.html")


def insumos(request):
	if request.method == "POST":
		miFormulario = InsumoFormulario(request.POST)
		print(miFormulario)

		if miFormulario.is_valid():
			informacion = miFormulario.cleaned_data
			insumos = Insumo(producto = informacion["producto"], cantidad = informacion["cantidad"])
			insumos.save()
			return render(request,"app_3er/index.html")
		
	else:
		miFormulario = InsumoFormulario()

	return render(request, "app_3er/insumos.html",{"miFormulario":miFormulario})


def about(request):
	return render(request, "app_3er/about.html")

def adoptantes(request):
	if request.method == "POST":
		miFormulario = AdoptanteFormulario(request.POST)
		print(miFormulario)

		if miFormulario.is_valid():
			informacion = miFormulario.cleaned_data
			adoptante = Adoptante(nombre = informacion["nombre"], apellido = informacion["apellido"],email = informacion["email"])
			adoptante.save()
			return render(request,"app_3er/index.html")
	
	else:
		miFormulario = AdoptanteFormulario()

	return render(request, "app_3er/adoptantes.html",{"miFormulario":miFormulario})
	

def busquedagato(request):
	return render(request, "app_3er/busquedagato.html")


def buscar(request):
	if request.GET['nombre']:
		nombre = request.GET['nombre']
		sexo = Adopcion.objects.filter(nombre__icontains=nombre)
		

		return render(request, "app_3er/resultado_busqueda_gato.html", {"nombre":nombre, "sexo":sexo})
	
	else:
		respuesta = "No enviaste datos"

	return HttpResponse(respuesta)
	
@login_required # para que solo los usuarios logeados puedan ver esta web
def leergatos(request):
	gatos = Adopcion.objects.all()
	contexto = {"gatos":gatos}
	return render(request, "app_3er/leergatos.html", contexto)

def borrargatos(request, gato_nombre):
	gato = Adopcion.objects.filter(nombre = gato_nombre)
	gato.delete()

	#vuelvo al menu
	gatos = Adopcion.objects.all()
	contexto = {"gatos":gatos}
	return render(request, "app_3er/leergatos.html", contexto)


def editargatos(request, gato_nombre):
    # Recibe el nombre del gato que vamos a modificar
    gato = Adopcion.objects.get(nombre=gato_nombre)

    # Si el método es POST, actualizamos el gato existente
    if request.method == "POST":
        miFormulario = AdopcionFormulario(request.POST, instance=gato)  # Pasamos la instancia del gato

        if miFormulario.is_valid():
            miFormulario.save()  # Guardamos los cambios en el objeto existente
            return render(request, "app_3er/index.html")

    else:
        miFormulario = AdopcionFormulario(instance=gato)  # Pasamos la instancia del gato

    return render(request, "app_3er/leergatos.html", {"miFormulario": miFormulario, "gato_nombre": gato_nombre})


class AdopcionList(ListView):
	model = Adopcion
	template_name = "app_3er/adopcion_list.html"

class AdopcionDetalle(DetailView):
	model = Adopcion
	template_name = "app_3er/adopcion_detalle.html"

class AdopcionCreacion(CreateView):
	model = Adopcion
	success_url = "app_3er/adopcion/list"
	fields = ['nombre','sexo']

class AdopcionUpdate(UpdateView):
	model = Adopcion
	success_url = "app_3er/adopcion/list"
	fields = ['nombre','sexo']

class AdopcionDelete(DeleteView):
	model = Adopcion
	success_url = "app_3er/adopcion/list"


# vistas para usuarios
# ----------------------------------------------------------------------------------------------------------------------------------------------

# pedido de login
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")

            user = authenticate(username=usuario, password=contra)

            if user is not None:
                login(request, user)
                return redirect("index")  # Redirigir a la URL con nombre "index"
            else:
                return render(request, "app_3er/index.html", {"mensaje": "Error, datos incorrectos"})

    else:
        form = AuthenticationForm()

    return render(request, "app_3er/login.html", {"form": form})



# para registrar un nuevo usuario
def registro(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"¡Usuario {username} creado exitosamente!")
            return redirect('index')
    else:
        form = UserRegisterForm()
    
    return render(request, "app_3er/registro.html", {"form": form})


#  mixin para que solo los usuarios que esten logeados puedan ver mi web
class ClaseQueNecesitaLogin(LoginRequiredMixin): 

	template_name = "leergatos.html"

@login_required
def editarperfil(request):
    # instancia del login
    usuario = request.user

    # si es método POST, hago lo mismo que en agregar
    if request.method == "POST":
        miFormulario = UserEditForm(request.POST)
        
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data

            # datos que se modifican
            usuario.email = informacion["email"]
            password = informacion["password1"]
            usuario.set_password(password)
            usuario.save()
            
            return render(request, "app_3er/index.html") # vuelvo al inicio o a donde quiera

    # en caso de que no sea POST
    else:
        # Creo un formulario con los datos que voy a modificar
        miFormulario = UserEditForm(initial={"email": usuario.email})

    # voy al HTML que me permite editar
    return render(request, "app_3er/editarperfil.html", {"miFormulario": miFormulario, "usuario": usuario})


@login_required
def agregaravatar(request):
    if request.method == 'POST':
        miFormulario = AvatarFormulario(request.POST, request.FILES)
        
        if miFormulario.is_valid():
            u = request.user

            try:
                avatar_existente = Avatar.objects.get(user=u)
                avatar_existente.delete()
            except Avatar.DoesNotExist:
                pass

            avatar = Avatar(user=u, imagen=miFormulario.cleaned_data['imagen'])
            avatar.save()

            return render(request, "app_3er/index.html")  # Volver a inicio o a donde quieras
    else:
        miFormulario = AvatarFormulario()  # Formulario vacío para construir el HTML

    return render(request, "app_3er/agregaravatar.html", {"miFormulario": miFormulario})


# blog ----------------------------------------------------------------

class ArticuloList(ListView):
    model = Articulo
    template_name = "app_3er/articulo_list.html"


class ArticuloDetalle(DetailView):
    model = Articulo
    template_name = "app_3er/articulo_detalle.html"

class ArticuloCreacion(LoginRequiredMixin, CreateView):
    model = Articulo
    template_name = "app_3er/articulo_creacion.html"
    fields = ['titulo', 'contenido']
    success_url = "/app_3er/blog/"  # URL a la que se redirige después de crear una nueva entrada

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class ArticuloUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articulo
    template_name = "app_3er/articulo_update.html"
    fields = ['titulo', 'contenido']
    success_url = "/app_3er/blog/"  # Especifica la URL de redirección

    def test_func(self):
        articulo = self.get_object()
        return self.request.user == articulo.autor


class ArticuloDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articulo
    template_name = "app_3er/articulo_delete.html"
    success_url = "/app_3er/blog/"  # Agrega la URL deseada aquí

    def test_func(self):
        articulo = self.get_object()
        return self.request.user == articulo.autor

    
    
