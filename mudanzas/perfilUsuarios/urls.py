from django.urls import path
from .views import perfil_usuario, editar_perfil

app_name = "perfilUsuarios"

urlpatterns = [
    path("", perfil_usuario, name="perfil_usuario"),        # /perfil/
    path("editar/", editar_perfil, name="editar_perfil"),   # /perfil/editar/
]