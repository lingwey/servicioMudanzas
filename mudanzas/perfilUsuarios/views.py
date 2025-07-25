from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Perfil
from .forms import PerfilForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from registroUsuarios.models import Usuario
from perfilUsuarios.models import Perfil

@login_required
def editar_perfil(request):
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("perfilUsuarios:perfil_usuario")  # redirige al perfil
    else:
        form = PerfilForm(instance=perfil)

    return render(request, "perfilUsuarios/editar_perfil.html", {"form": form})

@login_required
def perfil_usuario(request):
    perfil = Perfil.objects.filter(usuario=request.user).first()
    return render(request, "perfilUsuarios/perfil.html", {"usuario": request.user, "perfil": perfil})



def perfil_publico(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    perfil = Perfil.objects.filter(usuario=usuario).first()
    return render(request, "perfilUsuarios/perfil_publico.html", {"usuario": usuario,"perfil": perfil})
