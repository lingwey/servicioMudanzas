from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Cliente, ChoferParticular, Empresa

class RegistroUsuarioForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(choices=Usuario.TIPO_USUARIO_CHOICES, required=True, widget=forms.Select(attrs={'id': 'tipo_usuario'}))
    email = forms.EmailField(required=True)
    nombre = forms.CharField(max_length=150, required=True)
    dni = forms.CharField(max_length=8, required=False, widget=forms.TextInput(attrs={'id': 'dni_field'}))
    cuil = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={'id': 'cuil_field'}))

    # Campos de vehículo (solo chofer)
    tipo_vehiculo = forms.ChoiceField(
        choices=[("auto", "Auto"), ("van", "Van"), ("camion", "Camión")],
        required=False,
        widget=forms.Select(attrs={'id': 'tipo_vehiculo_field'})
    )
    numero_patente = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'id': 'patente_field'}))
    marca = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'id': 'marca_field'}))
    modelo = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'id': 'modelo_field'}))
    seguro = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'id': 'seguro_field'}))
    seguro_vigente = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'seguro_vigente_field'}))

    class Meta:
        model = Usuario
        fields = ["email", "nombre", "dni", "cuil", "tipo_usuario", "tipo_vehiculo", "numero_patente", "marca", "modelo", "seguro", "seguro_vigente", "password1", "password2"]

    def clean_numero_patente(self):
        """Verifica si la patente ya está registrada"""
        numero_patente = self.cleaned_data.get("numero_patente")
        if numero_patente and ChoferParticular.objects.filter(numero_patente=numero_patente).exists():
            raise ValidationError("Esta patente ya está registrada. Usa una diferente.")
        return numero_patente

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.tipo_usuario = self.cleaned_data["tipo_usuario"]
        usuario.username = usuario.email  # Usa email como username
        usuario.set_password(self.cleaned_data["password1"])  # Guarda la contraseña correctamente como hash

        # Asignación correcta según tipo de usuario
        if usuario.tipo_usuario == "cliente":
            usuario.dni = self.cleaned_data["dni"]
        elif usuario.tipo_usuario == "chofer_particular":
            usuario.dni = self.cleaned_data["dni"]
        elif usuario.tipo_usuario == "empresa":
            usuario.cuil = self.cleaned_data["cuil"]

        if commit:
            usuario.save()

            # Crear instancia específica según el tipo de usuario
            if usuario.tipo_usuario == "cliente":
                Cliente.objects.create(usuario=usuario)
            elif usuario.tipo_usuario == "chofer_particular":
                ChoferParticular.objects.create(
                    usuario=usuario,
                    tipo_vehiculo=self.cleaned_data["tipo_vehiculo"],
                    numero_patente=self.cleaned_data["numero_patente"],
                    marca=self.cleaned_data["marca"],
                    modelo=self.cleaned_data["modelo"],
                    seguro=self.cleaned_data["seguro"],
                    seguro_vigente=self.cleaned_data["seguro_vigente"]
                )
            elif usuario.tipo_usuario == "empresa":
                Empresa.objects.create(usuario=usuario)

        return usuario

    
#formulario para el login
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)