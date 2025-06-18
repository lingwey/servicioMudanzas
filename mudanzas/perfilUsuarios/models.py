from django.db import models
from registroUsuarios.models import Usuario

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)  # Cada usuario tiene un único perfil
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)  # Imagen de perfil opcional
    direccion = models.CharField(max_length=255)  # Dirección de residencia
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Teléfono de contacto
    fecha_nacimiento = models.DateField(blank=True, null=True)  # Fecha de nacimiento
    
    # Datos específicos por tipo de usuario
    registro_vehiculo = models.CharField(max_length=50, blank=True, null=True)  # Solo para choferes
    empresa_certificaciones = models.TextField(blank=True, null=True)  # Solo para empresas
    
    def __str__(self):
        return f"Perfil de {self.usuario.nombre} ({self.usuario.get_tipo_usuario_display()})"
