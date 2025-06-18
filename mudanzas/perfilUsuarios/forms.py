from django import forms
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["avatar", "direccion", "telefono", "fecha_nacimiento"]  # Campos editables
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
        }
