from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Usuario
from django.contrib.auth import login, authenticate
from perfilUsuarios.models import Perfil

"""# Formulario de login
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
"""
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
                return redirect("perfil_usuario")
            else:
                form.add_error(None, "Credenciales incorrectas")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})

# Vista para logout
"""@login_required
def logout_usuario(request):
    logout(request)
    return redirect("home")"""  # Redirige a la página de inicio después de cerrar sesión

# Vista protegida de perfil de usuario
"""@login_required
def perfil_usuario(request):
    perfil = Perfil.objects.filter(usuario=request.user).first()
    return render(request, "registroUsuarios/perfil.html", {"usuario": request.user, "perfil": perfil})"""

# control de registro de usuarios
def registro_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.backend = "registroUsuarios.authentication.EmailAuthBackend"
            login(request, usuario)  # Autenticamos al usuario después del registro
            return redirect("perfil_usuario")  # Redirige al perfil correctamente

    else:
        form = RegistroUsuarioForm()

    return render(request, "registroUsuario/registro.html", {"form": form})
