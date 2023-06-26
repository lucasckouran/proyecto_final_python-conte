from django.urls import path
from app_3er import views
# importaciones para usuarios
# ----------------------------------------------------------------------------------------------------------------------------------------------
from django.contrib.auth.views import LogoutView


urlpatterns = [
	path('', views.index, name = 'index'),
	path('adopciones/', views.adopciones, name = 'adopciones'),
	path('insumos/', views.insumos, name = 'insumos'),
	path('adoptantes/', views.adoptantes, name = 'adoptantes'),
    path('busquedagato/', views.busquedagato, name='busquedagato'),
    path('buscar/', views.buscar),
    path('leergatos/', views.leergatos, name="leergatos"),
    path('borrargatos/<str:gato_nombre>/', views.borrargatos, name='borrargatos'),
    path('editargatos/<str:gato_nombre>', views.editargatos, name="editargatos"),
    path('adopcion/list', views.AdopcionList.as_view(), name='List'),
	path(r'^(?P<pk>/d+)$', views.AdopcionDetalle.as_view(), name='Detail'),
	path(r'^nuevo$', views.AdopcionCreacion.as_view(), name='New'),
	path(r'^editar/(?P<pk>/d+)$', views.AdopcionUpdate.as_view(), name="Edit"),
	path(r'^borrar/(?P<pk>/d+)$', views.AdopcionDelete.as_view(), name='Delete'),
    path('login/', views.login_request, name="Login"),
    path('registro', views.registro, name="registro"),
    path('logout', LogoutView.as_view(template_name="app_3er/logout.html"), name = "Logout"),
    path('editarperfil', views.editarperfil, name="editarperfil"),
    path('agregaravatar/', views.agregaravatar, name="agregaravatar"),
    path('about/', views.about, name = 'about'),
    # Rutas para listar y ver detalles de los artículos
    path('blog/', views.ArticuloList.as_view(), name='articulo_list'),
    path('blog/<int:pk>/', views.ArticuloDetalle.as_view(), name='articulo_detail'),
    # Rutas para crear, editar y borrar artículos
    path('blog/nuevo/', views.ArticuloCreacion.as_view(), name='articulo_create'),
    path('blog/editar/<int:pk>/', views.ArticuloUpdate.as_view(), name='articulo_update'),
    path('blog/borrar/<int:pk>/', views.ArticuloDelete.as_view(), name='articulo_delete'),
    

]