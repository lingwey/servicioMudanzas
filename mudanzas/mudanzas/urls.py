from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from registroUsuarios.views import login_usuario
from perfilUsuarios.views import perfil_usuario
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),  # Panel de administración
    path("accounts/", include("django.contrib.auth.urls")),
    path("usuarios/", include("registroUsuarios.urls")),  # Enlace a la app de usuarios
    path("", lambda request: render(request, "home.html"), name="home"), 
    path("login/", login_usuario, name="login_usuario"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("perfil/", include("perfilUsuarios.urls", namespace="perfilUsuarios")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

