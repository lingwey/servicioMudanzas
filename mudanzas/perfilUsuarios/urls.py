from django.urls import path
from .views import perfil_usuario, editar_perfil, perfil_publico

app_name = "perfilUsuarios"

urlpatterns = [
    path("", perfil_usuario, name="perfil_usuario"),        # /perfil/
    path("editar/", editar_perfil, name="editar_perfil"),   # /perfil/editar/
    path("perfil/<int:user_id>/", perfil_publico, name="perfil_publico"),
]