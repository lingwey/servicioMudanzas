from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Usuario
from django.contrib.auth import login, authenticate
from perfilUsuarios.models import Perfil

# Vista para login
@csrf_protect
def login_usuario(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            usuario = authenticate(request, email=email, password=password)  # Usa `email` directamente

            if usuario is not None:
                login(request, usuario)  # Inicia sesión correctamente
                return redirect("perfilUsuarios:perfil_usuario")
            else:
                form.add_error(None, "Credenciales incorrectas")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})


# control de registro de usuarios
def registro_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.backend = "registroUsuarios.authentication.EmailAuthBackend"
            login(request, usuario)  # Autenticamos al usuario después del registro
            return redirect("perfilUsuarios:perfil_usuario")  # Redirige al perfil correctamente

    else:
        form = RegistroUsuarioForm()

    return render(request, "registroUsuario/registro.html", {"form": form})
